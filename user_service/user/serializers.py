from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import *



class RegisterUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = MyUser
        fields = ['email', 'password', 'confirm_password', 'account_type']

    def validate_email(self, value):
        if MyUser.objects.filter(email=value).exists():
              raise serializers.ValidationError('Account with this email already exists')
        return value
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
         
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = MyUser.objects.create_user(password=password, **validated_data)
        
        if user.account_type == 'individual':
            UserProfile.objects.create(user=user)
        elif user.account_type == 'company':
            UserProfile.objects.create(user=user)

        return user        
    
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({'non_field_errors': 'Both email and password are required'})
        
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError({'non_field_errors':'Wrong email or password'})
        
        attrs['user'] = user
        return attrs