from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(
        default='static/userProfile/default.jpg',
        upload_to='static/userProfile/',
        null=True,
        blank=True)
    status = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=10, default='student', null=True)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    students = models.ManyToManyField(
        User,
        related_name='students',
        blank=True)
    teacher = models.ForeignKey(
        User,
        related_name='teacher',
        null=True,
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    deadline = models.DateTimeField(null=True)
    available = models.BooleanField(default=True)

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='course_materials/')
    course = models.ForeignKey(
        Course,
        default='',
        on_delete=models.CASCADE)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    feedback = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    notification = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)