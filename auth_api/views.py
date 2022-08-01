from .serializer import *
# from rest_framework import status
from rest_framework import generics
from blog_api.models import post
# from .models import User_profile
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.shortcuts import render


def homeView(request):
    return render(request, "home.html")



class RegisterApiViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
