from rest_framework import serializers 
from app import models
from django.contrib.auth.models import User

class CourseSerializer(serializers.ModelSerializer):
    lecturer_name = serializers.CharField(source='lecturer.name')
    # creator_name = serializers.CharField(source='creator.first_name')
    creator = serializers.SerializerMethodField()
    CreateDate = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    TempletType = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    class Meta: 
        model = models.course 
        fields = ('CourseId', 'title', 'CreateDate', 'FilePath', 'progress', 'lecturer_name', 'GroupName','type','TempletType','creator','progress','FilePath','duration','SourceCourseId')
    
    def get_creator(self, obj):
        return obj.creator.first_name + obj.creator.last_name
    def get_CreateDate(self, obj):
        return obj.CreateDate.strftime('%Y-%m-%d')
    def get_type(self, obj):
        if obj.type=='a' :
            return '自筹'
        else :
            return obj.type  
    def get_TempletType(self, obj):
        if obj.TempletType=='slide' :
            return '三分屏'
        else :
            return obj.TempletType  
    def get_progress(self, obj):
        if obj.progress=='made' :
            return '未发布'
        elif obj.progress=='published':
            return '已发布'
        else :
            return obj.progress


class EditTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EditTask
        fields = ('id','course','TaskType','creator','CreateDate','TaskState','FinishedDate','TaskNote','ExtendedData')

class CourseTempletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseTemplet
        fields = ('id','name','note','customer')