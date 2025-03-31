from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Profile, Course, Material, Feedback, Notification
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try: #get profile
            profile = Profile.objects.get(user_id=request.user.id)
        except Profile.DoesNotExist: #if profile does not exist for the user, create profile
            profile = Profile(user_id=request.user.id)
            profile.save()
        courses = Course.objects.filter(students=request.user)
        teacher_courses = Course.objects.filter(teacher_id=request.user.id)

        template = loader.get_template('index.html')
        context = {'courses': courses, 'teacher_courses': teacher_courses, 'profile': profile}
        return HttpResponse(template.render(context, request))
    template = loader.get_template('loggedout.html')
    return HttpResponse(template.render({}, request))

# render chatroom
def room(request):
    return render(request, 'chatroom.html')

# render allCourses page
def allCourses(request):
    courses = Course.objects.all()
    template = loader.get_template('allCourses.html')
    context = {'courses': courses}
    return HttpResponse(template.render(context, request))

# render addCourse page
def addData(request):
    template = loader.get_template('addCourse.html')
    return HttpResponse(template.render({}, request))

def addCourse(request):
    name = request.POST.get('name')
    courses = Course.objects.all()

    course_names = []
    for i in courses: # get names of all the courses
        course_names.append(i.name)
    if name not in course_names: # if the course name does not exist
        course = Course(name=name)
        course.save()
        return HttpResponseRedirect(reverse('allCourses'))
    else:
        messages.info(request, 'Failed to add. This course already exists.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# render editCourse page
def editCourse(request):
    courses = Course.objects.all().values()
    template = loader.get_template('editCourse.html')
    context = {'courses': courses, 'user': request.user}
    return HttpResponse(template.render(context, request))

# delete course
def deleteCourse(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return HttpResponseRedirect(reverse('index'))

# render updateCourse page
def updateCourse(request, id):
    course = Course.objects.get(id=id)
    template = loader.get_template('updateCourse.html')
    context = {'course': course}
    return HttpResponse(template.render(context, request))

def updateCourseConfirmation(request, id):
    name = request.POST['name']
    deadline = request.POST['deadline']
    course = Course.objects.get(id=id)
    course.name = name
    course.deadline = deadline
    course.save()
    messages.info(request, 'Course successfully updated!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# render enrolCourse page
def enrolCourse(request):
    enrolled_courses = Course.objects.filter(students=request.user)
    courses = Course.objects.all()

    unenrolled = []
    for course in courses:
        if course not in enrolled_courses:
            unenrolled.append(course)

    template = loader.get_template('enrolCourse.html')
    context = {'unenrolled': unenrolled}
    return HttpResponse(template.render(context, request))

# add students to course
def enrol(request, courseid):
    course = Course.objects.get(id=courseid)
    course.students.add(request.user)

    if course.teacher:
        notification = Notification(user_id=course.teacher.id)
        notification.notification = 'New enrollment in ' + str(course.name)
        notification.save()

    return HttpResponseRedirect(reverse('index'))

# render coursePage
def coursePage(request, id):
    course = Course.objects.get(id=id)
    materials = Material.objects.filter(course_id=id)
    feedback = Feedback.objects.filter(course_id=id)
    template = loader.get_template('coursePage.html')
    context = {
        'course': course,
        'materials': materials,
        'feedback': feedback,
    }
    return HttpResponse(template.render(context, request))

# add teacher to course
def enrolTeacher(request, id):
    course = Course.objects.get(id=id)
    course.teacher_id = request.user.id
    course.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# upload course material in coursepage
def uploadMaterial(request, id):
    file = request.FILES['file']
    material = Material(file=file, course_id=id)
    material.save()

    course = Course.objects.get(id=id)

    for student in course.students.all():
        notification = Notification(user_id=student.id)
        notification.notification = "New upload in " + str(course.name)
        notification.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# download material file
def readMaterial(request, id):
    file = Material.objects.get(id=id)
    content = open('media/' + str(file.file)).read()
    return HttpResponse(content, content_type='text/plain')

# post feedback to course
def sendFeedback(request, courseid):
    profile = Profile.objects.get(user_id=request.user.id)
    course = Course.objects.get(id=courseid)
    feedback = request.POST['feedback']
    Feedback(feedback=feedback, course=course, profile=profile).save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def removeStudent(request, courseid, studentid):
    student = User.objects.get(id=studentid)
    course = Course.objects.get(id=courseid)
    course.students.remove(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# create profile and display edit profile page
def editProfilePage(request):
    user = request.user
    try: #get profile
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist: #if profile does not exist for the user, create profile
        profile = Profile(user_id=user.id)
        profile.save()
    template = loader.get_template('editProfile.html')
    context = {'profile': profile}
    return HttpResponse(template.render(context, request))

def updatePicture(request):
    profile = Profile.objects.get(user_id=request.user.id)
    image = request.FILES['image']
    profile.image = image
    profile.save()
    messages.info(request, 'Profile picture updated!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def updateName(request):
    user = request.user

    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    user.username = username
    user.first_name = first_name
    user.last_name = last_name

    user.save()
    messages.info(request, 'Name updated!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def updateStatus(request):
    profile = Profile.objects.get(user_id=request.user.id)

    status = request.POST['status']
    profile.status = status

    profile.save()
    messages.info(request, 'Status updated!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# render viewProfile page
def viewProfile(request, id):
    view = User.objects.get(id=id)
    courses = Course.objects.filter(students=view)
    teacher_courses = Course.objects.filter(teacher_id=view.id)

    template = loader.get_template('viewProfile.html')
    context = {'courses': courses, 'teacher_courses': teacher_courses, 'view': view}
    return HttpResponse(template.render(context, request))

# render searchPage
def searchPage(request):
    users = []
    search = request.POST['search']

    #split search string by whitespace
    names = search.split()
    #look for matching names in each field
    for name in names: 
        userName = User.objects.filter(username=name)
        firstName = User.objects.filter(first_name=name)
        lastName = User.objects.filter(last_name=name)
        if userName and userName[0] not in users and userName[0] != request.user:
                users.extend(userName)
        if firstName and firstName[0] not in users and firstName[0] != request.user:
                users.extend(firstName)
        if lastName and lastName[0] not in users and lastName[0] != request.user:
            users.extend(lastName)
    template = loader.get_template('searchPage.html')
    context = {'users': users,}
    return HttpResponse(template.render(context, request))

# render notifications page
def notifications(request):
    notifications = Notification.objects.filter(user_id=request.user.id)
    template = loader.get_template('notifications.html')
    context = {'notifications': notifications}
    return HttpResponse(template.render(context, request))