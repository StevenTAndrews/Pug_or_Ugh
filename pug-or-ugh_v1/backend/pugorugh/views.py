from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, generics, viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateDog(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        '''Retrieve dogs that match user pref.'''
        user = self.request.user
        user_pref = models.UserPref.objects.get(user=user)
        user_choice = self.kwargs.get('choice')
        preferred_dogs = Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size.split(','),
            age_group__in=user_pref.age
        )
        if choice == 'liked':
            queryset = preferred_dogs.filter(
                userdog__status='l',
                userdog__user_id=user.id
            )
        elif choice == 'disliked':
            queryset = preferred_dogs.filter(
                userdog__status='d',
                userdog__user_id=user.id
            )
        return queryset

    def get_object(self):
        return get_object_or_404(
            dog_id = self.get_queryset().filter(id__gt=pk).first(),
            pk=self.kwargs.get('pk')
        )

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        dog = get_object_or_404(models.Dog, pk=pk)
        user_choice = self.kwargs.get('choice')

        if user_choice == 'liked':
            choice = 'l'
        elif user_choice == 'disliked':
            choice = 'd'
        else:
            choice ='u'

        userdog = models.UserDog.objects.get(user=self.request.user, dog=dog)
        userdog.status = choice
        userdog.save()
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


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