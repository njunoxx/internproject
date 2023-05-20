from django.urls import path
from .views import UserRegistrationView, SuperUserRegistrationView, UserAuthenticationApi, \
AdminAttendanceUpdateApiIdView, UserUpdateView, AdminCreateAttendanceApi, UserAddAttendanceApiIdview, AttendanceApiIdView, \
PendingAttendanceApiIdView 


urlpatterns = [
    #Authenntication
    path('user-registration/', UserRegistrationView.as_view(), name="user-registration"),
    path('super-userregistration/', SuperUserRegistrationView.as_view(), name="superuser-registration"),
    path('login/', UserAuthenticationApi.as_view(), name='login'),
    path('logout/', UserAuthenticationApi.as_view(), name='logout'),
    #User Profile
    path('userprofile/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    #Attendance
    path('admin-attendance-create/', AdminCreateAttendanceApi.as_view(), name='admin-attendance-create'),
    path('admin-attendance-update/<int:id>/', AdminAttendanceUpdateApiIdView.as_view(), name='admin-attendance-update'),
    path('user-attendance-add/<int:id>/', UserAddAttendanceApiIdview.as_view(), name='user-attendance-add'),
    path('attendance-view/<int:id>/', AttendanceApiIdView.as_view(), name='attendance-view'),
    path('pending-attendance-view/<int:id>/', PendingAttendanceApiIdView.as_view(), name="pending-attendance-view"),
]