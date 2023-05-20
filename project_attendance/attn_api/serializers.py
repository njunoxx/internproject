from rest_framework import serializers
from app_attendance.models import CustomUser, Attendance
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
 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "email", "address", "contact", "gender")
        extra_kwargs = {'password': {'write_only':True, 'required':False}}

class UserAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id", "username", "date", "shift_start", "shift_end", "present")

class UseraddAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("date", "present")

# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'email', 'address', 'contact', 'gender')