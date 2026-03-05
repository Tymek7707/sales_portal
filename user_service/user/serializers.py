from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from django.db import IntegrityError

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
            CompanyProfile.objects.create(user=user)

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
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password' : 'old password is incorrect'})
        
        if new_password != confirm_new_password:
            raise serializers.ValidationError({'confirm_new_password' : 'New passwords must be the same'})
        
        if old_password == new_password:
            raise serializers.ValidationError({'new_password' : 'New password must be different than old password'})
        
        try:
            validate_password(new_password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        attrs['user'] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        return user



class SoftDeleteAccountSerializer(serializers.Serializer):
    reason = serializers.CharField(
        max_length=250,
        required = False,
        allow_blank = True,
        help_text = "Optional , why are you deleting account?"
        )
    confirm = serializers.BooleanField(
        required = True,
        help_text = 'are you sure to delete your account?'
        )

    def validate_confirm(self, val):
        if not val:
            raise serializers.ValidationError('You must confirm account deletion')
        return val


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ['email', 'account_type','phone_number', 'date_joined', 'id']
        read_only_fields = ['account_type' , 'date_joined', 'id']


        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user' , 'id']



class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['user' , 'id']
                