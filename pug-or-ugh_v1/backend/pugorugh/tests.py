from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Dog, UserDog, UserPref

# Create your tests here.
class TestDogModels(TestCase):
    def setUp(self):
        dog = Dog.objects.create(
            name='Frankie',
            image_filename='Frankie',
            breed='Pitbull',
            age=4
        )
        user = User.objects.create(
            username='Tester',
            password='testpassword'
        )
        userdog = UserDog.objects.create(
            user=user,
            dog=dog,
            status='l'
        )

    def test_dog_creation(self):
        dog = Dog.objects.get(name='Frankie')
        self.assertEqual('Frankie', dog.name)

    def test_user_pref_creation(self):
        self.assertNotEqual(self.userprefs, None)

    def test_userdog_creation(self):
        userdog = UserDog.objects.get(
            user=user,
            dog=dog
        )
        self.assertNotEqual(userdog, None)