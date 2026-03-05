from django.shortcuts import render
from django.utils import timezone

from rest_framework import status , generics
from rest_framework.exceptions import NotFound , PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

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
        user = serializer.validated_data['user']

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
        }, status=status.HTTP_200_OK)
    


class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):

        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'User logged out successfully'})
        except KeyError:
            return Response({'message': 'Refresh token is required'})
        except TokenError:
            return Response({'message': 'Invalid or expired token'})
        
class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data = request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'Password changed correctly'}, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)


class SoftDeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        serializer = SoftDeleteAccountSerializer(data = request.data)
        
        if serializer.is_valid(raise_exception=True):

            user = request.user

            user.is_active = False
            user.deleted_at = timezone.now()
            user.deletion_reason = serializer.validated_data.get('reason')
            user.save()




class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)
        return Response(serializer.data)
    


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer





class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile_and_serializer(self, user):
        
        if user.account_type == 'individual':
            try:
                profile = getattr(user, 'user_profile', None)
            except UserProfile.DoesNotExist:
                raise NotFound('Profile doesnt exist')
            return profile , UserProfileSerializer
        elif user.account_type == 'company':
            try:
                profile = getattr(user, 'company_profile', None)
            except CompanyProfile.DoesNotExist:
                    raise NotFound('Profile doesnt exist')
            return profile , CompanyProfileSerializer

    def get(self, request):

        user = request.user

        if user.is_staff or user.is_superuser:
            return Response(
            {
                "role": "admin",
                "email": user.email
            })
        
        profile , SerializerClass = self.get_profile_and_serializer(user)
        serializer = SerializerClass(profile)
        
        return Response(serializer.data)
    
    def patch(self, request):

        user = request.user

        if user.is_staff or user.is_superuser:
            raise PermissionDenied('Admin do not have editable profiles')
        
        profile , SerializerClass = self.get_profile_and_serializer(user)

        serializer = SerializerClass(profile, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)