from datetime import datetime,timedelta
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from datetime import datetime,timedelta
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .filters import *

def get_current_host(request):
    protocol=request.is_secure() and 'https' or 'http'
    host=request.get_host()
    return f"{protocol}://{host}/"

@api_view(['POST'])
def new_course(request):
    data=request.data
    serializer=CourseSerializer(data=data)
    if serializer.is_valid():
       course=Course.objects.create(**data)
       res=CourseSerializer(course,many=False)
       return Response({"Created Course":res.data})
    else:
        return Response({serializer.errors})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_course_video(request):
    data=request.data
    student=request.user
    new_course_object=get_object_or_404(Course,name=data['course'])
    host=get_current_host(request)
    domain=new_course_object.id
    token = get_random_string(40)
    new_course_object.video_token=token
    expire_date = datetime.now() + timedelta(minutes=120)
    new_course_object.video_expire=expire_date
    new_course_object.student=student
    new_course_object.save()
    return Response({'Course Link':f'{host}/college/videolink/{domain}',"Course id":new_course_object.id},status=status.HTTP_201_CREATED)




@api_view(['GET'])
def access_course_video(request,pk):
    course=get_object_or_404(Course,id=pk)
    print(course.video_expire.replace(tzinfo=None))
    print(datetime.now())
    min_left=course.video_expire.replace(tzinfo=None) - datetime.now()
    min_left=int(min_left.seconds/60)
    if datetime.now() > course.video_expire.replace(tzinfo=None):
        return Response({"Video has expired":"Please try again later"},status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"Video":"Video","Minutes left:":min_left},status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def bruh(request):
    data=request.data
    nam=data['name']
    student=get_object_or_404(Student,name=nam)
    serializer=StudentSerializer(student,many=False)
    return Response({"Student details":serializer.data})

@api_view(['GET'])
def view_courses(request):
    courses=Course.objects.all()
    serializer=CourseSerializer(courses,many=True)
    return Response({"Courses:":serializer.data})


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    link = f"http://localhost:8000/college/reset_password/{token}".format(token=token)
    body = f"Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})




@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token=token)
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({"error":"Token has expired"},status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirmPassword']:
        return Response({"error":"Passwords do not match"},status=status.HTTP_400_BAD_REQUEST)
     
    user.password= make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({'details': 'Password successfully reset'})


@api_view(['POST'])
def student_register(request):
    data=request.data
    user = UserSerializer(data = data)
    if user.is_valid():  
        user = User.objects.create(
        email=data['email'],
        password=make_password(data['password']),
        username=data['username'],
        )  
        user.save()
        student=Student.objects.create( 
        name=data['name'],
        year=data['year'],
        major=data['major'],
        user=user
        )
        student.save()  
        return Response({"Details":user.username},status=status.HTTP_201_CREATED)
    else:
         return Response({"Not valid": user.errors}, status=status.HTTP_400_BAD_REQUEST)



        
     



@api_view(['GET'])
def check_user(request):
    courses=CoursessFilter(request.GET,queryset=Course.objects.all().order_by('id'))
    c=courses.qs.count()
    paginator=PageNumberPagination()
    paginator.page_size=1
    queryset=paginator.paginate_queryset(courses.qs,request)
    serializer=StudentCourseSerializer(queryset,many=True)
    return Response({'Course User':serializer.data})
    

        



    