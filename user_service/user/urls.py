from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('change_password/', ChangeUserPasswordView.as_view(), name='change_password'),
    path('delete_account/',SoftDeleteAccountView.as_view(), name='soft_delete'),
    path('me/', UserView.as_view(), name = 'me'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh')
]