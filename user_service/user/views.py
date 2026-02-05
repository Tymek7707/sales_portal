from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
# Create your views here.

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message' : 'User registered succesfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(TokenObtainPairView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data('user')

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'user' : {
                'id' : user.id,
                'email' : user.email,
                'type' : user.account_type,

            },
            'refresh': str(refresh_token),
            'access': access_token,
        }
        )