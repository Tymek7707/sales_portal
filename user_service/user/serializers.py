from rest_framework import serializers

from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email' , 'date_joined']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class 