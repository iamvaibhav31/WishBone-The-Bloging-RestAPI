from .views import *
from django.urls import path
# from knox.views import LogoutView , LogoutAllView
# from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
  path("",homeView,name="home view"),
  # path('user_info/' , get_user_data.as_view() , name= 'user profile' ), 
  path('register/' , RegisterApiViews.as_view() , name= 'Register user' ),
  path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]