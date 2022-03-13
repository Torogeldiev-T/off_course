from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (("Teacher", "Teacher"), ("Student", "Student"))


class User(AbstractUser):
    role = models.CharField(choices=ROLE_CHOICES, max_length=8)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
