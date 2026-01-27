from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
# Create your models here.


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True , max_length=80)
    
    phone_number = models.CharField(max_length=9, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = 
class UserProfile(models.Model):
    avatar = models.ImageField(null=True)
    
    city = models.CharField(max_length=80)
    
    bio = models.TextField(blank=True)

class CompanyProfile(models.Model):
    avatar = models.ImageField(null=True)
    
    city = models.CharField(max_length=80)
    nip = models.CharField(max_length=10)

    bio = models.TextField(blank=True)