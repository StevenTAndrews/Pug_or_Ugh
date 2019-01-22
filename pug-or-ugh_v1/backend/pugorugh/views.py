from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions, generics, viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    '''Retrieve and update UserPref instances'''
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user=self.request.user)

    def put(self, request, *args, **kwargs):
        user_pref = self.get_object()
        pref_serializer = serializers.UserPrefSerializer(
            user_pref, request.data)
        if pref_serializer.is_valid():
            pref_serializer.save()
            return Response(pref_serializer.data)
        return Response(pref_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDogView(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        user_pref = models.UserPref.objects.get(user=user)
        decision = self.kwargs.get('decision')
        preferred_dogs = models.Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size.split(','),
            age_group__in=user_pref.age
        )
        if decision == 'undecided':
            queryset = preferred_dogs.filter(
                userdog__status='u',
                userdog__user_id=user.id,
            ).order_by('pk')
        elif decision == 'liked':
            queryset = preferred_dogs.filter(
                userdog__status='l',
                userdog__user_id=user.id
            ).order_by('pk')
        elif decision == 'disliked':
            queryset = preferred_dogs.filter(
                userdog__status='d',
                userdog__user_id=user.id
            ).order_by('pk')
        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()
        dog = queryset.filter(id__gt=pk).first()
        if dog is not None:
            return dog
        return queryset.first()

    def get(self, request, decision, pk, format=None):
        dog = self.get_object()
        serializer = serializers.DogSerializer(dog)
        print("Length of queryset: %s " % len(self.get_queryset()))
        print(self.get_queryset())
        print("PK sent to Django: %s " % pk)
        print("\n" * 2)
        if not dog:
            raise Http404
        return Response(serializer.data)

class DecisionView(generics.UpdateAPIView):
    '''Update UserDog instances with new status based on arguments from the URL'''
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        dog = get_object_or_404(models.Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, decision, *args, **kwargs):
        if decision == 'undecided':
            decision = 'u'
        elif decision == 'liked':
            decision = 'l'
        elif decision == 'disliked':
            decision = 'd'
        dog = self.get_object()
        obj, exists = models.UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={
                'user': self.request.user,
                'dog': dog,
                'status': decision
            }
        )
        if obj:
            obj.status = decision
            obj.save()
        return Response("Okay!")
