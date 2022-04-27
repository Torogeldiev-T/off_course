from django.db import models
from accounts.models import Creator
from django.contrib.auth.models import User
from courses.models import Course

class Invitation(models.Model):
    creator_from = models.ForeignKey(Creator, on_delete=models.CASCADE)
    email_to = models.CharField(max_length=150) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)

    is_checked = models.BooleanField(default=False)
    is_accepted = models.BooleanField()
    

