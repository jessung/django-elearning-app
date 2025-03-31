from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Material, Profile, Feedback, Notification

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'image', 'status', 'role')
    
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    students = UserSerializer(many=True)
    teacher = UserSerializer()

    class Meta:
        model = Course
        fields = ('id', 'students', 'teacher', 'name', 'deadline', 'available')

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Material
        fields = ('id', 'file', 'course')

class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer()
    profile = ProfileSerializer()

    class Meta:
        model = Feedback
        fields = ('id', 'feedback', 'course', 'profile', 'created_at')

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'notification', 'user', 'created_at')