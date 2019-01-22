from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        '''Create user and user pref'''
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user_pref = models.UserPref.objects.create(user=user)
        user_pref.save()
        user.save()
        self.user_dog_status(user)
        return user

    def user_dog_status(self, user):
        '''Create userdog status to undecided'''
        dogs = models.Dog.objects.all()
        for dog in dogs:
            user_dog = models.UserDog.objects.create(
                user=user,
                dog=dog,
                status='u'
            )
            user_dog.save()


    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
        )
        model = models.Dog


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'age',
            'gender',
            'size',
        )
        model = models.UserPref

class UserDogSerializer(serializers.ModelSerializer):
    dog = DogSerializer
    class Meta:
        field = (
            'user',
            'dog',
            'status'
        )
        model = models.UserDog
