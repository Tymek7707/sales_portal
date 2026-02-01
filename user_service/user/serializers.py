from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from .models import *



class RegisterUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = MyUser
        fields = ['email', 'password', 'confirm_password', 'account_type']

    def validate_email(self, value):
        if MyUser.objects.filter(email=value):
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
        user.save()

        return user        