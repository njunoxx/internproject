from app_attendance.models import CustomUser, Attendance
from .serializers import UserRegistrationSerializer, SuperUserRegistrationSerializer, UserProfileSerializer, \
UserAttendanceSerializer, UseraddAttendanceSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#from rest_framework.permissions import IsAuthenticated

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
        if not request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = CustomUser.objects.all()
            serializer = SuperUserRegistrationSerializer(user, many=True)
            return Response(CustomResponse.successResponse(200, "User List", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
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


@method_decorator(login_required, name="dispatch")
class UserUpdateView(APIView):
    def get_object(self, id):
        try:
            data = CustomUser.objects.get(id=id)
            return data
        except CustomUser.DoesNotExist:
            return None
        
    def get(self, request, id):
        if not request.user.is_superuser:
            instance = self.get_object(id)
            if not instance:
                return Response({"Message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            if request.user.id != id:
                return Response({"msg":"Unauthorized Access"}, status=status.HTTP_401_UNAUTHORIZED)
            user = CustomUser.objects.filter(id=id)
            serializer = UserProfileSerializer(user, many=True)
            return Response(CustomResponse.successResponse(200, "User Lists", serializer.data), status=status.HTTP_200_OK)
        else:
            user = CustomUser.objects.all()
            serializer = UserProfileSerializer(user, many=True)
            return Response(CustomResponse.successResponse(200, "User List", serializer.data), status=status.HTTP_200_OK)
    
    def put(self, request, id):
        if not request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        if not request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            instance = self.get_object(id)
            if not instance:
                return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            instance.delete()
            return Response({"msg":"Deleted Successfully"}, status=status.HTTP_200_OK)

@method_decorator(login_required, name="dispatch")
class AdminCreateAttendanceApi(APIView):
    def get(self, request): 
       if request.user.is_superuser:
            att = Attendance.objects.all()
            serializer = UserAttendanceSerializer(att, many=True)
            return Response(CustomResponse.successResponse(200, "User Attendance", serializer.data), status=status.HTTP_200_OK)
       else:
           return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
       
    def post(self, request):
        if not request.user.is_superuser:
            return Response({"Error":"Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        shift_start = request.POST.get('shift_start')
        shift_end = request.POST.get('shift_end')
        data = {
            "username" : request.POST.get('username'),
            "date" : request.POST.get('date'),
            "shift_start": shift_start,
            "shift_end": shift_end,
        }
        serializer = UserAttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# admin le attendance create garney     
@method_decorator(login_required, name="dispatch")
class AdminAttendanceUpdateApiIdView(APIView):
    def get_object(self, id):
        try:
            data = Attendance.objects.get(id=id)
            return data
        except Attendance.DoesNotExist:
            return None
        
    def get(self, request, id):
        if not request.user.is_superuser:
            instance = self.get_object(id)
            if not instance:
                return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserAttendanceSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            att = Attendance.objects.all()
            serializer = UserAttendanceSerializer(att, many=True)
            return Response(CustomResponse.successResponse(200, "User Attendance", serializer.data), status=status.HTTP_200_OK)

    def put(self, request, id):
        if not request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        shift_start = request.POST.get('shift_start')
        shift_end = request.POST.get('shift_end')
        data = {
            "username" : request.POST.get('username'),
            "date" : request.POST.get('date'),
            "shift_start": shift_start,
            "shift_end": shift_end,
        }
        serializer = UserAttendanceSerializer(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        if not request.user.is_superuser:
            return Response({"Message":"Unauthorized Access!!!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            instance = self.get_object(id)
            if not instance:
                return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            instance.delete()
            return Response({"msg":"Deleted Successfully"}, status=status.HTTP_200_OK)
    
class UserAddAttendanceApiIdview(APIView):
    def get_object(request, id):
        try:
            data = Attendance.objects.get(id=id)
            return data
        except Attendance.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        att = Attendance.objects.filter(username=request.user, present=False)
        serializer = UserAttendanceSerializer(att, many=True)
        return Response(CustomResponse.successResponse(200, "Attendance Lists", serializer.data), status=status.HTTP_200_OK)
    
    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        data = {
            # "username" : request.POST.get('username'),
            "date" : request.POST.get('date'),
            # "shift_start": request.POST.get('shift_start'),
            # "shift_end": request.POST.get('shift_end'),
            "present": True if request.POST.get('present')=="present" else False,
        }
        serializer = UseraddAttendanceSerializer(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AttendanceApiIdView(APIView):
    def get_object(requset, id):
        try:
            data = CustomUser.objects.get(id=id)
            return data
        except CustomUser.DoesNotExist:
            return None
        
    def get(self, request, id):
        att = Attendance.objects.filter(username=id, present=True)
        serializer = UserAttendanceSerializer(att, many=True)
        return Response (CustomResponse.successResponse(200, "Attendance Lists", serializer.data), status=status.HTTP_200_OK)

class PendingAttendanceApiIdView(APIView):
    def get_object(requset, id):
        try:
            data = CustomUser.objects.get(id=id)
            return data
        except CustomUser.DoesNotExist:
            return None
        
    def get(self, request, id):
        att = Attendance.objects.filter(username=id, present=False)
        serializer = UserAttendanceSerializer(att, many=True)
        return Response(CustomResponse.successResponse(200, "Attendance Lists", serializer.data), status=status.HTTP_200_OK)

class AdminAttendanceCreateApiid(APIView):
    def get_object(self, id):
        try:
            data = CustomUser.object.get(id=id)
            return data
        except CustomUser.DoesNotExist:
            return None
        
    
