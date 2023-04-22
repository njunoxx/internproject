from rest_framework import serializers
from app_attendance.models import CustomUser
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "address", "contact", "gender")
      
    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email',),
            address=validated_data.get('address'),
            contact=validated_data.get('contact'),
            gender=validated_data.get('gender'),
        )
        return user
        
class SuperUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "email", "address", "contact", "gender")

    def create(self, validated_data):
        user = CustomUser.objects.create_superuser(
        username=validated_data['username'],
        password=validated_data['password'],
        email=validated_data.get('email',),
        address=validated_data.get('address'),
        contact=validated_data.get('contact'),
        gender=validated_data.get('gender'),    
        )
        return user