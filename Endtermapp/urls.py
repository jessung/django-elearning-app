from django.urls import path, include
from rest_framework import routers
# from .views import *
from .import views
from .apis import *

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'course', CourseViewSet)
router.register(r'material', MaterialViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'notification', NotificationViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('chatroom/', views.room, name='room'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # get apis
    path('api/getUser/<int:id>', getUser, name='getUser'),
    path('api/getCourse/<int:id>', getCourse, name='getCourse'),
    path('api/getProfile/<int:id>', getProfile, name='getProfile'),
    path('api/getFeedback/<int:id>', getFeedback, name='getFeedback'),
    path('api/getNotification/<int:id>', getNotification, name='getNotification'),
    path('api/allCourses/<int:id>', allCourses, name='allCourses'),
    # post apis
    path('api/addCourse/<int:id>', addCourse, name='addCourse'),
    path('api/sendFeedback/<int:id>', sendFeedback, name='sendFeedback'),
    path('api/uploadMaterial/<int:id>', uploadMaterial, name='uploadMaterial'),
    path('api/createNotification/<int:id>', createNotification, name='createNotification'),
    # delete apis
    path('api/deleteUser/<int:id>', deleteUser, name='deleteUser'),
    path('api/deleteCourse/<int:id>', deleteCourse, name='deleteCourse'),
    path('api/deleteFeedback/<int:id>', deleteFeedback, name='deleteFeedback'),
    path('api/deleteNotification/<int:id>', deleteNotification, name='deleteNotification'),
    # put apis
    path('api/updateCourse/<int:id>', updateCourse, name='updateCourse'),
    path('api/enrolStudent/<int:id>', enrolStudent, name='enrolStudent'),
    path('api/enrolTeacher/<int:id>', enrolTeacher, name='enrolTeacher'),
    path('api/updateName/<int:id>', updateName, name='updateName'),
    path('api/removeStudent/<int:id>', removeStudent, name='removeStudent'),
    path('api/updateStatus/<int:id>', updateStatus, name='updateStatus'),

    # edit course
    path('addData/', views.addData, name='addData'),
    path('addData/addCourse/', views.addCourse, name='addCourse'),
    path('allCourses/', views.allCourses, name='allCourses'),
    path('editCourse/', views.editCourse, name='editCourse'),
    path('deleteCourse/<int:id>', views.deleteCourse, name='deleteCourse'),
    path('updateCourse/<int:id>', views.updateCourse, name='updateCourse'),
    path('updateCourse/updateCourseConfirmation/<int:id>', views.updateCourseConfirmation, name='updateCourseConfirmation'),
    path('enrolCourse/', views.enrolCourse, name='enrolCourse'),
    path('enrolCourse/enrol/<int:courseid>', views.enrol, name='enrol'),
    
    # render course page and apis
    path('coursePage/<int:id>', views.coursePage, name='coursePage'),
    path('coursePage/enrolTeacher/<int:id>', views.enrolTeacher, name='enrolTeacher'),
    path('coursePage/removeStudent/<int:courseid>/<int:studentid>', views.removeStudent, name='removeStudent'),
    path('coursePage/sendFeedback/<int:courseid>', views.sendFeedback, name='sendFeedback'),
    path('coursePage/uploadMaterial/<int:id>', views.uploadMaterial, name='uploadMaterial'),
    path('coursePage/readMaterial/<int:id>', views. readMaterial, name='readMaterial'),

    # render editProfile page and update profile apis
    path('editProfilePage/', views.editProfilePage, name='editProfilePage'),
    path('editProfilePage/updatePicture/', views.updatePicture, name='updatePicture'),
    path('editProfilePage/updateName/', views.updateName, name='updateName'),
    path('editProfilePage/updateStatus/', views.updateStatus, name='updateStatus'),

    # render other user's profile
    path('viewProfile/<int:id>', views.viewProfile, name='viewProfile'),

    # render search page and results
    path('searchPage/', views.searchPage, name='searchPage'),

    #render notifications page
    path('notifications/', views.notifications, name='notifications'),

]