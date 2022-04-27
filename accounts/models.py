from django.db import models
from courses.models import Subject
from django.contrib.auth.models import User

ROLE_CHOICES = (("Teacher", "Teacher"), ("Student", "Student"))


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth = models.DateField()
    university = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(birth__gte="1900-01-01")
                & models.Q(birth__lte="2022-01-01"),
                name="ch_st_birth_from_01-01-1900_to_01-01-2022",
            )
        ]


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth = models.DateField()

    specialized_subjects = models.ManyToManyField(Subject, related_name="teachers")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(birth__gte="1900-01-01")
                & models.Q(birth__lte="2022-01-01"),
                name="ch_tc_birth_from_01-01-1900_to_01-01-2022",
            )
        ]


class Creator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creators")
