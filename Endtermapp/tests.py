from rest_framework.test import APITestCase
from django.urls import reverse

import json
from rest_framework import status
from django.test import TestCase, Client
from .models import Profile, Course, Material, Feedback, Notification
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, CourseSerializer, MaterialSerializer, FeedbackSerializer, UserSerializer, NotificationSerializer


client = Client()

# Create your tests here.
class TestAppModels(APITestCase):
    def setUp(self):
        #set up users
        self.user1 = User.objects.create(username="teacher1", first_name="John", last_name="Ng")
        self.user2 = User.objects.create(username="student1", first_name="Jane", last_name="Ng")
        self.user3 = User.objects.create(username="student2", first_name="Joe", last_name="Ng")
        #set up profiles
        self.profile1 = Profile.objects.create(user_id=self.user1.id, role="teacher")
        self.profile2 = Profile.objects.create(user_id=self.user2.id, role="student")
        self.profile3 = Profile.objects.create(user_id=self.user3.id, role="student")
        #set up course
        self.course1 = Course.objects.create(name="course1")
        self.course2 = Course.objects.create(name="course2")
        #set up feedback
        self.feedback = Feedback.objects.create(feedback="new feedback", 
                                                course_id=self.course1.id, 
                                                profile_id=self.profile1.id)
        #set up notifications
        self.notification = Notification.objects.create(notification="new notif")

    def testUser(self):
        self.assertEqual(str(self.user1.username), "teacher1")
        self.assertEqual(str(self.user1.first_name), "John")
        self.assertEqual(str(self.user1.last_name), "Ng")
    def testProfile(self):
        self.assertEqual(str(self.profile1.user_id), str(self.user1.id))
        self.assertEqual(str(self.profile1.role), "teacher")
    def testCourse(self):
        self.assertEqual(str(self.course1.name), "course1")
    def testFeedback(self):
        self.assertEqual(str(self.feedback.feedback), "new feedback")
        self.assertEqual(str(self.feedback.course_id), str(self.course1.id))
        self.assertEqual(str(self.feedback.profile_id), str(self.profile1.id))
    def testNotification(self):
        self.assertEqual(str(self.notification.notification), "new notif")

    # test get
    def testGetUser(self):
        response = client.get(reverse('getUser', args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user1)
        self.assertEqual(response.data, serializer.data)
    def testGetCourse(self):
        response = client.get(reverse('getCourse', args=[self.course1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CourseSerializer(self.course1)
        self.assertEqual(response.data, serializer.data)
    def testGetProfile(self):
        response = client.get(reverse('getProfile', args=[self.profile1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProfileSerializer(self.profile1)
        self.assertEqual(response.data, serializer.data)
    def testGetFeedback(self):
        response = client.get(reverse('getFeedback', args=[self.feedback.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = FeedbackSerializer(self.feedback)
        self.assertEqual(response.data, serializer.data)
    def testGetNotification(self):
        response = client.get(reverse('getNotification', args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = NotificationSerializer(self.notification)
        self.assertEqual(response.data, serializer.data)

    # # test post 
    # def testAddCourse(self):
    #     data = {
    #         'name': 'new course',
    #         'teacher': self.user1
    #     }
    #     # response = self.client.post(reverse('addCourse',kwargs={'id':self.course1.id,}), data, content_type='application/json')
    #     # response = client.post(reverse('addCourse', args=[self.course1.id]), data)
    #     response = client.post(reverse('addCourse', args=[self.course1.id]), data)

    #     # response = self.client.post('/api/addCourse/{self.course1.id}', data)

    #     # response = self.client.post('addCourse', data)
    #     # response = self.client.post('/api/addCourse/{self.course1.id}', data)

    #     # print('hi', data, self.course1.name)
    #     # print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['name'], 'new course')
    # def testSendFeedback(self):
    #     data = {
    #         'feedback': 'hi',
    #         'course': self.course1,
    #         'profile': self.profile1,
    #     }
    #     response = self.client.post('/api/sendFeedback/{self.feedback.id}', data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['feedback'], 'hi')
        
    # test put
    # def testUpdateCourse(self):
    #     data = {
    #         'name': 'updatename'
    #     }
    #     response = self.client.put('/api/updateCourse/1', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'updatename')


        
    # test delete
    def testDeleteUser(self):
        response = client.delete(reverse('deleteUser', args=[self.user1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def testDeleteCourse(self):
        response = client.delete(reverse('deleteCourse', args=[self.course1.id]), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def testDeleteFeedback(self):
        response = client.delete(reverse('deleteFeedback', args=[self.feedback.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def testDeleteNotification(self):
        response = client.delete(reverse('deleteNotification', args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)