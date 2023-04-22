from django.urls import path
from .import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('userregister/', views.create_normal_user, name='user-register'),
    path('adminregister/', views.create_admin_user, name='admin-register'),
    path('login/', views.user_login, name='login'),
    path('addattendance/', views.add_attendance, name='attendance-add'),
    path('logout/', views.user_logout, name='logout'),
    path('attendanceview/', views.attendance_view, name='attendance-view'),
    path('attendanceedit/<int:id>/', views.edit_attendance, name='attendance-edit'),
    path('attendancedelete/<int:id>/', views.delete_attendance, name='attendance-delete'),
    path('userprofile/', views.user_profile, name='user-profile'),
    path('useredit/<int:id>/', views.user_edit, name='user-edit'),
    path('userdelete/<int:id>/', views.user_delete, name='user-delete'),
]