from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from app_attendance.models import CustomUser
from .serializers import UserRegistrationSerializer, SuperUserRegistrationSerializer
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class CustomResponse():
    def successResponse(self, code, msg, data=dict()):
        context = {
            "status_code" : code,
            "message" : msg,
            "data" : data,
            "error" : []
        }
        return context
    


class UserRegistrationView(APIView):
    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserRegistrationSerializer(user, many=True)
        return Response(CustomResponse.successResponse(200, "User List", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data={
                'response': "Successfully registers normal user",
                'username': user.username,
                'password': user.password,
                'email':user.email,
                'address': user.address,
                'contact': user.contact,
                'gender' :user.gender
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuperUserRegistrationView(APIView):
    def get(self, request):
        user = CustomUser.objects.all()
        serializer = SuperUserRegistrationSerializer(user, many=True)
        return Response(CustomResponse.successResponse(200, "User List", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SuperUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data={
                'response': "Successfully registers Super user",
                'username': user.username,
                'password': user.password,
                'email':user.email,
                'address': user.address,
                'contact': user.contact,
                'gender' :user.gender
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthenticationApi(APIView):
    def get(self, request):
        user = request
        logout(user)
        return Response({"Message": "Logged Out successfully!"}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"Message": "Logged in successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Username or Password doesnot match!!!"}, status=status.HTTP_400_BAD_REQUEST)
