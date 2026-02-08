from django.urls import path

from .views import *
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('me/', UserView.as_view(), name = 'me'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('my_profile/', MyProfileView.as_view(), name='my_profile')
]