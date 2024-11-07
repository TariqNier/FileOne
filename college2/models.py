import random
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext
# Create your models here.


class Majors(models.TextChoices):
    CS ='CS','Computer Science'
    ENG = 'ENG','Engineering'
    BNS= 'BNS', "Business"
    MED ='MED','Medicene'
    COM = 'COM', 'Communication'
    ART= 'ART', 'Art & Design'
    
class Year(models.IntegerChoices):
    first=1
    second=2
    third=3
    fourth=4
    fifth=5
    sixth=6
  
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True,blank=True)  
  


  
    
class Student(models.Model):
    name = models.TextField(max_length=40,default="",blank=False)
    year = models.IntegerField(choices=Year.choices,blank=False)
    SID = models.IntegerField(unique=True,primary_key=True,default="",blank=True,editable=False)
    major = models.CharField(max_length=40,choices=Majors.choices,blank=False)
    user = models.OneToOneField(User,related_name='student',on_delete=models.CASCADE)
    registered_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.SID:
            self.SID= self.generate_sid()
        super().save(*args,**kwargs)
    
    
    def generate_sid(self):
        while True:
            sid = random.randint(100000, 999999) 
            if not Student.objects.filter(SID=sid).exists():  
                return sid

class Course(models.Model):
    name=models.TextField(max_length=40,blank=False,default="")   
    video_token = models.CharField(max_length=50,default="",blank=True)
    video_expire = models.DateTimeField(null=True,blank=True)
    course_year=models.IntegerField(choices=Year.choices,null=True,blank=False,)
    course_major=models.CharField(max_length=50,choices=Majors.choices,null=True,blank=False)
    # user=models.ForeignKey(User,null=True,on_delete=models.PROTECT)
    student=models.ForeignKey(Student,null=True,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name         
            
class Teacher(models.Model):
    name = models.TextField(max_length=40,default="",blank=False)
    user = models.OneToOneField(User,related_name='teacher',on_delete=models.CASCADE)
    registered_at=models.DateTimeField(auto_now_add=True)
    course=models.OneToOneField(Course,on_delete=models.PROTECT,max_length=60)
    
    
@receiver(post_save, sender=User)
def save_profile(sender,instance, created, **kwargs):
    user = instance

    if created:
        profile = Profile(user = user)
        profile.save()

   

    
     
    
    
    


