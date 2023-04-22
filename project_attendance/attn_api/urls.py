from django.urls import path
from .views import UserRegistrationView, SuperUserRegistrationView, UserAuthenticationApi

urlpatterns = [
    path('userregistration/', UserRegistrationView.as_view(), name="user-registration"),
    path('superuserregistration/', SuperUserRegistrationView.as_view(), name="superuser-registration"),
    path('login/', UserAuthenticationApi.as_view(), name='login'),
    path('logout/', UserAuthenticationApi.as_view(), name='logout'),
]