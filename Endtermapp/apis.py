from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer, CourseSerializer, MaterialSerializer, UserSerializer, FeedbackSerializer, NotificationSerializer
from .models import Profile, Course, Material, Feedback, Notification
from django.contrib.auth.models import User
from django.contrib import messages

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer()

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer()

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer()

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer()

# get course
@api_view(['GET'])
def getCourse(request, id):
    try:
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return HttpResponse(status=404)

# get profile
@api_view(['GET'])
def getProfile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)
    
# get user
@api_view(['GET'])
def getUser(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
# get feedback
@api_view(['GET'])
def getFeedback(request, id):
    try:
        feedback = Feedback.objects.get(id=id)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)
    except Feedback.DoesNotExist:
        return HttpResponse(status=404)


# get notification
@api_view(['GET'])
def getNotification(request, id):
    try:
        notifications = Notification.objects.get(id=id)
        serializer = NotificationSerializer(notifications)
        return Response(serializer.data)
    except Notification.DoesNotExist:
        return HttpResponse(status=404)

# get all of a user's courses
@api_view(['GET'])
def allCourses(request, id):
    try:
        courses = Course.objects.filter(user_id=id)
        serializer = CourseSerializer(courses)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return HttpResponse(status=404)

# delete course
@api_view(['GET', 'DELETE'])
def deleteCourse(request, id):
    try:
        course = Course.objects.get(id=id)
        if request.method == 'DELETE':
            course.delete()
            return Response(status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = CourseSerializer(course)
            return Response(serializer.data)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# delete user
# there is no delete profile as deleting the user also deletes the profile
@api_view(['GET', 'DELETE'])
def deleteUser(request, id):
    try:
        user = User.objects.get(id=id)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# delete feedback
@api_view(['GET', 'DELETE'])
def deleteFeedback(request, id):
    try:
        feedback = Feedback.objects.get(id=id)
        if request.method == 'DELETE':
            feedback.delete()
            return Response(status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# delete notification
@api_view(['GET', 'DELETE'])
def deleteNotification(request, id):
    try:
        notification = Notification.objects.get(id=id)
        if request.method == 'DELETE':
            notification.delete()
            return Response(status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# update course
@api_view(['GET', 'PUT'])
def updateCourse(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

# add students to course
@api_view(['GET', 'PUT'])
def enrolStudent(request, courseid, userid):
    try:
        course = Course.objects.get(id=courseid)
        user = User.objects.get(id=userid)
    except Course.DoesNotExist or User.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        course.students.add(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

# add teacher to course
@api_view(['GET', 'PUT'])
def enrolTeacher(request, courseid, userid):
    try:
        course = Course.objects.get(id=courseid)
    except Course.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        course.teacher_id = userid
        course.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = UserSerializer(course)
        return Response(serializer.data)
    
# add new course
@api_view(['GET', 'POST'])
def addCourse(request, id):
    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

# upload course material
@api_view(['GET', 'POST'])
def uploadMaterial(request, id):
    if request.method == 'POST':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        material = Material.objects.get(id=id)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

# add feedback to course
@api_view(['GET', 'POST'])
def sendFeedback(request, id):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        feedback = Feedback.objects.get(id=id)
    except Feedback.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)
    
# add feedback to course
@api_view(['GET', 'POST'])
def createNotification(request, id):
    if request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        notification = Notification.objects.get(id=id)
    except Notification.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

# remove student from course
@api_view(['GET', 'PUT'])
def removeStudent(request, courseid, studentid):
    try:
        student = User.objects.get(id=studentid)
        course = Course.objects.get(id=courseid)
    except User.DoesNotExist or Course.DoesNotExist:
        return HttpResponse(status=404)
    course.students.remove(student)
    serializer = CourseSerializer(course)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# update user name, first name and last name
@api_view(['GET', 'PUT'])
def updateName(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

# update profile status
@api_view(['GET', 'PUT'])
def updateStatus(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
