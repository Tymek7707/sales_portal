from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin

from .managers import UserManager
from .validators import *
# Create your models here.


class MyUser(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
    ]

    username = None
    email = models.EmailField(unique=True , max_length=80)

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
    )   
    phone_number = models.CharField(max_length=9, unique=True, null=True, blank=True, validators=[validate_phone_number])
     
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class BaseProfile(models.Model):
    city = models.CharField(max_length=80, validators=[validate_only_letters])
    
    bio = models.TextField(blank=True)

    class Meta:
        abstract = True


class UserProfile(BaseProfile):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user_profile',
        )
    
    first_name = models.CharField(max_length=50, null=True , blank=True, validators=[validate_only_letters])
    last_name = models.CharField(max_length=50, null=True, blank=True, validators=[validate_only_letters])

    date_of_birth = models.DateField(null=True ,blank=True)



class CompanyProfile(BaseProfile):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='company_profile',
        )

    company_name = models.CharField(max_length=100, null=True)        

    nip = models.CharField(max_length=10, validators=[validate_nip], null=True)