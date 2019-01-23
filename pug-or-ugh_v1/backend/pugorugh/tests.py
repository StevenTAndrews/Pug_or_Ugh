from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from .models import Dog, UserDog, UserPref
from . import views

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Dog.objects.create(
            name='Frankie',
            image_filename='1.jpg',
            breed='Pitbull',
            age=50,
            gender='f',
            size='m'
        )
        User.objects.create(
            username='Tester',
            password='testpassword'
        )

    def test_dog_creation(self):
        dog = Dog.objects.get(name='Frankie')
        self.assertEqual(dog.name, 'Frankie')
        self.assertEqual(dog.image_filename, '1.jpg')
        self.assertEqual(dog.breed, 'Pitbull')
        self.assertEqual(dog.age, 50)
        self.assertEqual(dog.gender, 'f')
        self.assertEqual(dog.size, 'm')
        self.assertEqual(dog.age_group, 'a')

    def test_user_pref_creation(self):
        user = User.objects.get(username='Tester')
        user_pref = UserPref.objects.create(age='b,a',
                                            gender='m,f',
                                            size='m',
                                            user=user)
        self.assertEqual(user_pref.user, user)
        self.assertEqual(user_pref.age, 'b,a')
        self.assertEqual(user_pref.gender, 'm,f')
        self.assertEqual(user_pref.size, 'm')

    def test_user_dog_creation(self):
        user = User.objects.get(username='Tester')
        dog = Dog.objects.get(name='Frankie')
        user_dog = UserDog.objects.create(user=user,
                                          dog=dog,
                                          status='l')
        self.assertEqual(user_dog.user, user)
        self.assertEqual(user_dog.dog, dog)
        self.assertEqual(user_dog.status, 'l')


class ViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        Dog.objects.create(
                name='Frankie',
                image_filename='1.jpg',
                breed='Pitbull',
                age=50,
                gender='f',
                size='m'
        )
        User.objects.create(username='Tester', password='testpassword')

    def test_user_register(self):
        url = reverse('register-user')
        data = {'username': 'TestTester', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'TestTester')
        self.assertTrue(User.objects.get(id=2).check_password('testpassword'))

    def test_like_dog(self):
        kwargs = {'pk': '1', 'decision': 'liked'}
        url = reverse('decide', kwargs=kwargs)
        user = User.objects.get(username='Tester')
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 200)