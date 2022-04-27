from django.db import models
import accounts
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from .fields import OrderField
from . import grades

MODULE_CHOICES = (
    ("Assignment", "Assignment"),
    ("Test", "Test"),
    ("Quiz", "Quiz"),
    ("Topic", "Topic"),
)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    creator = models.ForeignKey(
        "accounts.Creator",
        related_name="courses_created",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # key to enroll to the course, must be kept in secret
    enrollement_key = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.FloatField()

    # link to invite teachers to participate in the course, must be kept in secret

    class Meta:
        ordering = ["-created"]
        constraints = [
            models.CheckConstraint(
                name="ch_price_gte_zero", check=models.Q(price__gte=0.0)
            )
        ]

    def __str__(self):
        return self.title


class StudentCourseRate(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scale = models.FloatField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(scale__gte=0.0) & models.Q(scale__lte=10.0),
                name="ch_scale_from_zero_to_ten",
            )
        ]


class StudentCourseGrade(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE)
    teacher = models.ForeignKey("accounts.Teacher", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(
        max_length=11, choices=grades.STUDENT_COURSE_GRADES, default=grades.NOT_GRADED
    )


class CourseParticipant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE)

    is_finished = models.BooleanField(default=False)
    enrolled = models.DateTimeField(auto_now_add=True)

    grade = models.ForeignKey(
        StudentCourseGrade, on_delete=models.SET_DEFAULT, default=grades.NOT_GRADED
    )

    rate = models.ForeignKey(StudentCourseRate, on_delete=models.SET_NULL, null=True)


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey("accounts.Teacher", on_delete=models.CASCADE)

    enrolled = models.DateTimeField(auto_now_add=True)


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "video",
                "image",
                "file",
                "quiz",
                "assignment",
                "topic",
            )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()
