from django.urls import path
from . import views

urlpatterns=[
    
    path("videos/",views.get_course_video,name="get_course_video"),
    path("newcourse/",views.new_course,name="new_course"),
    path("bruh/",views.bruh,name="bruh"),
    path("videolink/<str:pk>",views.access_course_video,name="access_course_link"),
    path("viewcourses/",views.view_courses,name="view_courses"),
    path("register/",views.student_register,name="student_register"),
    path("checkuser/",views.check_user,name="check_user"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("reset_password/<str:token>",views.reset_password,name="reset_password"),
    
    
]