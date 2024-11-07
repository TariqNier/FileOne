from rest_framework import serializers
from .models import *
from django.utils.translation import gettext as _

class MySerializer(serializers.Serializer):
    message = serializers.CharField(default=_("Hello, this is a localized message!"))



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"
        
# class CourseUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Course
#         fields=('user','name')

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=('student','name')
            
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"