"""
Definition of models.
"""

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User 
#from app.CustomClass import ModelsFields
from django_pgjsonb import JSONField

# Create your models here.

class course(models.Model):
    CourseId=models.CharField(max_length=100,primary_key=True)
    title=models.CharField(max_length=200)
    GroupName=models.CharField(max_length=200,null=True)
    creator= models.ForeignKey(User,on_delete=models.CASCADE)
    CreateDate=models.DateTimeField(default=timezone.now())
    MakeDate=models.DateTimeField(null=True)
    ProjectId=models.CharField(max_length=100,null=True)
    FilePath=models.CharField(max_length=1024,null=True)
    SlideVersion=models.CharField(max_length=100,null=True)
    type=models.CharField(max_length=100,null=True)
    TempletType=models.CharField(max_length=100,default="slide")
    duration=models.IntegerField(null=True)
    SourceCourseId=models.ForeignKey("course",null=True,on_delete=models.CASCADE)
    EpisodeCount=models.IntegerField(null=True)
    lecturer=models.ForeignKey("lecturer",null=True,on_delete=models.CASCADE)
    PublishCategory = models.ManyToManyField("PublishCategory") 
    InternalCategory = models.ManyToManyField("InternalCategory") 
    progress=models.CharField(max_length=100,null=True)
    KeyWords=models.CharField(max_length=1024,null=True)
    note=models.CharField(max_length=200,null=True)
    ExtendedData = JSONField(null=True)
    subtitles = JSONField(null=True)

class ReEditCourse(models.Model):
    CourseId=models.CharField(max_length=100,primary_key=True)
    title=models.CharField(max_length=200)
    GroupName=models.CharField(max_length=200,null=True)
    creator= models.ForeignKey(User,on_delete=models.CASCADE)
    CreateDate=models.DateTimeField(default=timezone.now())
    MakeDate=models.DateTimeField(null=True)
    ProjectId=models.CharField(max_length=100,null=True)
    FilePath=models.CharField(max_length=1024,null=True)
    SlideVersion=models.CharField(max_length=100,null=True)
    type=models.CharField(max_length=100,null=True)
    TempletType=models.CharField(max_length=100,default="slide")
    duration=models.IntegerField(null=True)
    SourceCourseId=models.ForeignKey("ReEditCourse",null=True,on_delete=models.CASCADE)
    EpisodeCount=models.IntegerField(null=True)
    lecturer=models.ForeignKey("lecturer",null=True,on_delete=models.CASCADE)
    PublishCategory = models.ManyToManyField("PublishCategory") 
    InternalCategory = models.ManyToManyField("InternalCategory") 
    progress=models.CharField(max_length=100,null=True)
    KeyWords=models.CharField(max_length=1024,null=True)
    note=models.CharField(max_length=200,null=True)
    ExtendedData = JSONField(null=True)
    subtitles = JSONField(null=True)    

class CourseLog(models.Model):
    course = models.ForeignKey("course",null=True,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.CharField(max_length=100)
    date=models.DateTimeField(default=timezone.now())
    log = JSONField(null=True)

class CourseAbstract(models.Model):
    course=models.ForeignKey("course",on_delete=models.CASCADE)
    index=models.IntegerField(validators=[MaxValueValidator(50)])
    Text=models.CharField(max_length=2048,null=True)
    class Meta:
        unique_together = ("course", "index") #约束 非主键
        #index_together = ("course", "index")  #联合唯一索引

class InternalCategory(models.Model):
    InternalCategoryId=models.CharField(max_length=100,primary_key=True)
    name=models.CharField(max_length=200)
    parent=models.ForeignKey("InternalCategory",null=True,on_delete=models.CASCADE)
    path=models.CharField(max_length=1024,null=True)
    note=models.CharField(max_length=200,null=True)

class PublishCategory(models.Model):
    PublishCategoryId=models.CharField(max_length=100,primary_key=True)
    type=models.CharField(max_length=200)
    name=models.CharField(max_length=200)

class lecturer(models.Model):
    LecturerId=models.CharField(max_length=100,primary_key=True)
    name=models.CharField(max_length=100)
    post=models.CharField(max_length=300,null=True)
    introduction=models.CharField(max_length=2048,null=True)
    PhotoSrc=models.CharField(max_length=1024,null=True)
    IntroSrc=models.CharField(max_length=1024,null=True)
    note=models.CharField(max_length=200,null=True)

class EditTask(models.Model):
    #course=models.ForeignKey(course,null=True)
    course=models.ManyToManyField(course)
    TaskType=models.CharField(max_length=100)
    TaskPriority=models.CharField(max_length=100,default="A")
    creator= models.ForeignKey(User,on_delete=models.CASCADE)
    #CreateDate=models.DateTimeField(auto_now=True)#更新其他列，此列时间自动更新
    #CreateDate=models.DateTimeField(default=timezone.now())#时间不即时更新
    CreateDate=models.DateTimeField(auto_now_add=True)#
    TaskState=models.CharField(max_length=100)
    FinishedDate=models.DateTimeField(null=True)
    TaskNote=models.TextField(null=True)
    ExtendedData=models.TextField(null=True)
    #ExtendedData=models.CharField(max_length=2048,null=True)
    customer= models.ForeignKey("customer",null=True,on_delete=models.CASCADE)

class customer(models.Model):
    name=models.CharField(max_length=200)
    sort=models.CharField(max_length=50)
    area=models.CharField(max_length=20)

class CourseTemplet(models.Model):
    name=models.CharField(max_length=100)
    customer=models.ForeignKey("customer",null=True,on_delete=models.CASCADE)
    FilePath=models.CharField(max_length=1024)
    note=models.CharField(max_length=500)


