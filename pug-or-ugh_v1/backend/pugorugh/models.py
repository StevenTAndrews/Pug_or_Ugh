from django.contrib.auth.models import User
from django.db import models


'''Gender Options'''
MALE = 'm'
FEMALE = 'f'
UNKNOWN = 'u'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNKNOWN, 'Unknown')
)


'''Dog size options'''
SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
EXTRA_LARGE = 'xl'
UNKNOWN = 'u'
SIZE_CHOICES = (
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
    (EXTRA_LARGE, 'Extra Large'),
    (UNKNOWN, 'Unknown')
)


'''Like or Dislike options'''
LIKED = 'l'
DISLIKED = 'd'
STATUS_CHOICES = (
    (LIKED, 'Like'),
    (DISLIKED, 'Dislike')
)

'''Age Options'''
BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'
AGE_CHOICES = (
    (BABY, 'Baby'),
    (YOUNG, 'Young'),
    (ADULT, 'Adult'),
    (SENIOR, 'Senior'),
)



class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='Unknown mix')
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)


class UserPref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, default='b,y,a,s')
    gender = models.CharField(max_length=3, default='f,m')
    size = models.CharField(max_length=10, default='s,m,l,xl')
