from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=10)

    objects = UserManager()

    REQUIRED_FIELDS = []

class Attendance(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    hours_worked = models.DurationField()
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.username)
    
    class Meta:
        db_table = "app_attendance"