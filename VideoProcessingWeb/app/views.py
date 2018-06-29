"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

import os
import ntpath
import re
import time
import json
import codecs
import base64
import urllib
import shutil
import requests
from xml.dom.minidom import parse
import xml.dom.minidom
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from app import models
from app.CustomClass import JsonSuite
from app.CustomClass import CommonMethod
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from VideoProcessingWeb.settings import STATIC_ROOT
from VideoProcessingWeb.settings import COURSE_ROOT
from VideoProcessingWeb.settings import COURSE_TEMP
from VideoProcessingWeb.settings import COURSE_URL
from VideoProcessingWeb.settings import LECTURER_ROOT
from VideoProcessingWeb.settings import LECTURER_URL
from VideoProcessingWeb.settings import DOC_ROOT
from VideoProcessingWeb.settings import ProjectCollection_URL
from django.db.models import Q
import pymysql
from django.http import FileResponse
#REST OP
from rest_framework import viewsets, serializers, permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import list_route
from rest_framework_jwt.utils import jwt_decode_handler
from app.CustomClass import RestSerializers
#REST ED

# CsrfExempt OP
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication

#class CsrfExemptSessionAuthentication(TokenAuthentication):
#    def enforce_csrf(self, request):
#        return  # To not perform the csrf check previously happening
# CsrfExempt ED

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

#VideoUpload
def VideoUpload(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        ret = {'status': False, 'data': None, 'error': None}
        try:
            title = request.POST.get('fileTitle')
            file = request.FILES.get('fileInput')
            id=time.strftime('%Y%m%d%H%M%S')
            #
            NewCourse = models.course(CourseId=id,title=title)
            NewCourse.save()
            ret['data'] = 'DB_Success'
            #
            #path = "course" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
            path = COURSE_ROOT + id + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            DestinationFilePath = path + 'source'+ os.path.splitext(file.name)[1] 
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in file.chunks():
                DestinationFile.write(chunk)
            ret['status'] = True
            ret['data'] = 'DB_Upload_Success'
            DestinationFile.close()
            #
            #NewTask = models.EditTask(course=NewCourse,TaskType='STT',TaskState='WaitingToBegin')
            NewTask = models.EditTask(TaskType='STT',TaskState='WaitingToBegin')
            NewTask.save()
            NewTask.course.add(NewCourse)
            NewTask.save()
            ret['data'] = 'DB1_Upload_DB2_Success'
            #
        except Exception as e:
            ret['error'] = str(e)
        finally:   
            #return HttpResponse(json.dumps(ret))
            #return HttpResponse(ret)
            return HttpResponseRedirect('/TaskQuery')  
    return render(request, 'app/VideoUpload.html')

def AjaxVideoUploadPage(request):
    CourseTitle = request.GET.get('CourseTitle')
    return render(request, 'app/VideoUpload.html',{'temvarCourseTitle':CourseTitle})   #这里upload_page便是上面的前端html文件

def AjaxVideoUpload(request):
    ret = {'status': False, 'data': None, 'error': None}
    try:
            title = request.POST.get('thisFileTitle')
            file = request.FILES['thisFileInput']
            id=time.strftime('%Y%m%d%H%M%S')
            #
            NewCourse = models.course(CourseId=id,title=title)
            NewCourse.save()
            ret['data'] = 'DB_Success'
            #
            #path = "course" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
            path = COURSE_FILE_PATH + id + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            DestinationFilePath = path + 'source'+ os.path.splitext(file.name)[1] 
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in file.chunks():
                DestinationFile.write(chunk)
            ret['status'] = True
            ret['data'] = 'DB_Upload_Success'
            DestinationFile.close()
            #
            #NewTask = models.EditTask(course=NewCourse,TaskType='STT',TaskState='WaitingToBegin')
            NewTask = models.EditTask(TaskType='STT',TaskState='WaitingToBegin')
            NewTask.save()
            NewTask.course.add(NewCourse)
            NewTask.save()
            ret['data'] = 'DB1_Upload_DB2_Success'
            #
    except Exception as e:
            ret['error'] = str(e)
    finally:   
            #return HttpResponse(json.dumps(ret))
            #return HttpResponse(ret)
            return HttpResponse()
    
#Split File Upload
def FTPVideoUpload_backup(request):
    assert isinstance(request, HttpRequest)
    #Login OP
    if request.user.is_authenticated():
        # Do something for authenticated users.
        CurrentUser=request.user.username
    else: 
        # Do something for anonymous users.
        LoginStr = request.GET.get('link')
        if CommonMethod.LinkLogin(LoginStr)!=False:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
        else:    
            return HttpResponseRedirect('/login')   
    #Login ED
    #Upload OP
    if request.method == 'POST':
        file = request.FILES.get('FileInput')
        CourseTitle = request.POST.get('CourseTitle')
        ProjectId = request.POST.get('ProjectId')
        lecturer=request.POST.get('lecturer')
        WorkType=request.POST.get('WorkType')
        CourseId=request.POST.get('CourseId')
        #FTP OP
        ''' ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect('ftp://newpms.cei.cn', 21)
        ftp.login('CourseFtp@newpms.cei.cn', 'ftp@2018')
        ftp.mkd(CourseId)
        bufsize = 1024
        fp = open(file[0], 'rb')
        ftp.storbinary('STOR ' + CourseId +'mp4', fp, bufsize)
        fp.close() '''
        #FTP ED
        #File OP
        FileTotal = request.POST.get('total')
        FileIndex = request.POST.get('index')
        path = COURSE_ROOT + CourseId[0:4] + '/' + CourseId + '/'
        TempPath = path + 'temp/'
        if not os.path.exists(TempPath):
            os.makedirs(TempPath)
        DestinationFilePath =  TempPath + 'raw_' + FileIndex +'.mp4'
        DestinationFile = open(DestinationFilePath, 'wb+')
        for chunk in file.chunks():
             DestinationFile.write(chunk)
        DestinationFile.close()
        #File ED
        if FileIndex==FileTotal :
            #Join OP
            outfile = open(os.path.join(path,'raw.mp4'),'wb')
            files = os.listdir(TempPath) #list all the part files in the directory
            if len(files)==int(FileTotal) :
            #files.sort(reverse=True)                #sort part files to read in order
            #for file in files:
            #    filepath = os.path.join(TempPath,file)
            #    infile = open(filepath,'rb')
            #    data = infile.read()
            #    outfile.write(data)
            #    infile.close()
                for CurrentIndex in range(1,int(FileTotal)):
                    filepath = os.path.join(TempPath,'raw_' + str(CurrentIndex) +'.mp4')
                    infile = open(filepath,'rb')
                    data = infile.read()
                    outfile.write(data)
                    infile.close()
                outfile.close()
                shutil.rmtree(TempPath)
            #Join ED
            #TYPE
            if 1==1:
                #Data OP
                NewCourse = models.course(CourseId=CourseId,title=CourseTitle,FilePath='/'+ CourseId[0:4] + '/',note=lecturer,type=WorkType,ProjectId=ProjectId,progress='VideoUploaded')
                NewCourse.save()
                #NewTask = models.EditTask(course=NewCourse,TaskType='STT',TaskState='WaitingToBegin')
                NewTask = models.EditTask(TaskType='STT',TaskState='WaitingToBegin')
                NewTask.save()
                NewTask.course.add(NewCourse)
                NewTask.save()
                #Data ED    
    #Upload ED        
    #Page OP        
    else:
        CourseTitle = urllib.parse.unquote(request.GET.get('title','X'))     
        ProjectId=urllib.parse.unquote(request.GET.get('ProjectNo','X'))  
        lecturer=urllib.parse.unquote(request.GET.get('lecturer'))  
        WorkType=request.GET.get('type')  
        CourseId=time.strftime('%Y%m%d%H%M%S')+(''.join(re.findall("[a-z,A-Z,0-9]+", ProjectId)))
        return render(request, 'app/FTPVideoUpload.html',{'temvarCourseTitle':CourseTitle
                                                        ,'temvarProjectId':ProjectId
                                                        ,'temvarLecturer':lecturer
                                                        ,'temvarWorkType':WorkType
                                                        ,'temvarCourseId':CourseId})   
    #Page ED    
    return render(request, 'app/FTPVideoUpload.html')

def FTPVideoUpload(request):
    assert isinstance(request, HttpRequest)
    #Login OP
    if request.user.is_authenticated():
        # Do something for authenticated users.
        CurrentUser=request.user.username
        DBUser=User.objects.get(username=CurrentUser) 
    else: 
        # Do something for anonymous users.
        LoginStr = request.GET.get('link')
        if CommonMethod.LinkLogin(LoginStr)!=False:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
            DBUser=User.objects.get(username=user.username) 
        else:    
            return HttpResponseRedirect('/login')   
    #Login ED
    ret = {'status': False, 'data': None, 'error': None}
    ProjectId=urllib.parse.unquote(request.GET.get('ProjectNo','X'))
    SourcePath = COURSE_TEMP + ProjectId + '.mp4'
    #RipPath = COURSE_TEMP + ProjectId + '_s.mp4'
    #if not (os.path.exists(SourcePath) and os.path.exists(RipPath)):
    if not (os.path.exists(SourcePath)):
        ret['error'] = 'File not found'
        return HttpResponse(json.dumps(ret))
    else:
        CurrentCourse = models.course.objects.filter(ProjectId=ProjectId)
        if CurrentCourse: 
            CourseId=CurrentCourse[0].CourseId
        else:
            CourseId=time.strftime('%Y%m%d%H%M%S')+(''.join(re.findall("[a-z,A-Z,0-9]+", ProjectId)))
        CourseTitle = urllib.parse.unquote(request.GET.get('title','X'))     
        lecturer=urllib.parse.unquote(request.GET.get('lecturer'))  
        WorkType=request.GET.get('type')   
        path = COURSE_ROOT + CourseId[0:4] + '/' + CourseId + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        #目标存在时,shutil.move()报错    
        if os.path.exists(path+'raw.mp4'):
            os.remove(path+'raw.mp4')
        if os.path.exists(path+'rip.mp4'):
            os.remove(path+'rip.mp4')
        shutil.move(SourcePath,path+'raw.mp4')
        #shutil.move(RipPath,path+'rip.mp4')
        #if (os.path.exists(path+'raw.mp4') and os.path.exists(path+'rip.mp4')):
        if (os.path.exists(path+'raw.mp4')):
            ret['status'] = '文件验证通过'
    #TYPE
    if 1==1:
        #DATA OP
        if(models.course.objects.filter(CourseId=CourseId).count()==0):
            NewCourse = models.course(CourseId=CourseId,title=CourseTitle,FilePath='/'+ CourseId[0:4] + '/',note=lecturer,type=WorkType,ProjectId=ProjectId,progress='FileUploaded',creator=DBUser)
            NewCourse.save() 
        else:
            NewCourse = models.course.objects.get(CourseId=CourseId)
        #NewTask = models.EditTask(course=NewCourse,TaskType='VideoCheckEncoder',TaskState='WaitingToBegin')
        NewTask = models.EditTask(TaskType='VideoCheckEncoder',TaskState='WaitingToBegin',creator=DBUser)
        NewTask.save()
        NewTask.course.add(NewCourse)
        NewTask.save()
        ret['data'] = '数据添加成功'              
         #DATA ED    
    return HttpResponse(json.dumps(ret,ensure_ascii=False))
  
#PlayVideo
def PlayVideo(request):
    assert isinstance(request, HttpRequest)
    #Login OP
    if request.user.is_authenticated():
        # Do something for authenticated users.
        CurrentUser=request.user.username
        DBUser=User.objects.get(username=CurrentUser) 
    else: 
        # Do something for anonymous users.
        LoginStr = request.GET.get('link')
        if CommonMethod.LinkLogin(LoginStr)!=False:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
            DBUser=User.objects.get(username=user.username) 
        else:    
            return HttpResponseRedirect('/login')   
    #Login ED
    if request.method == 'POST':
        ProjectId = request.POST.get('projectId')
        CurrentCourse = models.course.objects.get(ProjectId=ProjectId)
        CurrentCourse.progress= 'VideoFileChecked'
        CurrentCourse.save()
        #NewTask = models.EditTask(course=CurrentCourse,TaskType='STT',TaskState='WaitingToBegin')
        NewTask = models.EditTask(TaskType='STT',TaskState='WaitingToBegin',creator=DBUser)
        NewTask.save()
        NewTask.course.add(CurrentCourse)
        NewTask.save()
        return HttpResponse('审核完毕')
    else:    
        ProjectId = request.GET.get('ProjectNo')
        CurrentCourse = models.course.objects.filter(ProjectId=ProjectId)
        CourseId=CurrentCourse[0].CourseId
        TaskCount=models.EditTask.objects.filter(course=CurrentCourse[0],TaskType='STT').count()
        path = COURSE_URL + CourseId[0:4] + '/' + CourseId + '/'
        return render(request,'app/PlayVideo.html',{'VideoFilePath' :path+'rip.mp4',
                                                    'RawVideoFilePath' :path+'raw.mp4',
                                                    'temvarIsTaskExists':TaskCount,
                                                    'temvarProjectId':ProjectId})

# Query
@login_required
def TaskQuery(request):
    assert isinstance(request, HttpRequest)
    TaskItems = models.EditTask.objects.all()
    return render(request,'app/TaskQuery.html',{'li':TaskItems})

def STTEditList(request):
    assert isinstance(request, HttpRequest)
    TaskItems = models.EditTask.objects.filter(
        TaskType="STT",
        TaskState="Finished")
    return render(request,'app/TaskQuery.html',{'li':TaskItems,
                                                'JobType':"编辑文本",
                                                'OperationLink':"CaptionsEdit/?id="})

def VideoSegmentList(request):
    assert isinstance(request, HttpRequest)
    DataItems = models.course.objects.all()
    return render(request,'app/CourseQuery.html',{'li':DataItems,
                                                'JobType':"编辑分割点",
                                                'OperationLink':"VideoSegment/?id="})

def CourseQuery(request):
    assert isinstance(request, HttpRequest)
    DataItems = models.course.objects.filter(progress="made")
    return render(request,'app/CourseQuery.html',{'li':DataItems,
                                                'JobType1':"下载",
                                                'OperationLink1':"/CourseHandle/?id=",
                                                'JobType2':"发布",
                                                'OperationLink2':"/CourseHandle/?id=",
                                                'JobType3':"取消发布",
                                                'OperationLink1':"/CourseHandle/?id="
                                                })      

def CourseHandle(request):
    assert isinstance(request, HttpRequest)
    ret = {}
    id = request.GET.get('id')
    ThisCourse = models.course.objects.get(CourseId=id)
    shutil.copytree(COURSE_ROOT + id[0:4] + '/' + id + '/',COURSE_TEMP + id + '/')
    ret['Url']= 'ftp://203.207.197.16/' + id + '/'
    return JsonResponse(ret) 

def MyTask(request):
    assert isinstance(request, HttpRequest)
    TaskItems = models.EditTask.objects.filter(
        TaskType="STT",
        TaskState="Finished")
    return render(request,'app/MyTask.html',
                  {'Editli':TaskItems,
                   'Checkli':TaskItems,
                   'Publishli':TaskItems,
                   'JobType':"选定", 
                   'EditLink':"SlideEdit/?id=000",
                   'CheckLink':"CourseUpload/?id=",
                   'PublishLink':"CourseUpload/?id="}
                  )

#STTEdit
def STTEdit(request):
    assert isinstance(request, HttpRequest)
    id = request.GET.get('id')
    path = COURSE_FILE_PATH + id + '/'
    ServerPath = COURSE_FILE_SERVER_PATH + id + '/'
    with open(path+'STT.json', 'r+', encoding='utf-8') as JsonText:
        #JsonDate = json.dumps(JsonText.read(),ensure_ascii=False)
        JsonObj = json.loads(JsonText.read())
        ListDate=[]
        for i in range(0, len(JsonObj["results"])):
            DictThis={}
            DictThis["StartTime"]=str(JsonObj["results"][i]["alternatives"][0]["timestamps"][0]).split(",")[1]
            DictThis["EndTime"]=(str(JsonObj["results"][i]["alternatives"][0]["timestamps"][len(JsonObj["results"][i]["alternatives"][0]["timestamps"])-1])).split(",")[2][:-1]
            DictThis["Text"]=str(JsonObj["results"][i]["alternatives"][0]["transcript"])
            ListDate.append(DictThis)
        #return HttpResponse(JsonObj["results"][0]["alternatives"][0]["timestamps"][0])
        return render(request,'app/STTEdit.html',{'li':ListDate,
                                                   'VideoFilePath' :ServerPath+'source.mp4'})
    return render(request,'app/STTEdit.html')

#CaptionsEdit
def CaptionsEdit(request):
    assert isinstance(request, HttpRequest)
    id = request.GET.get('id')
    path = os.path.join(COURSE_FILE_PATH, 'temp/')
    ServerPath = COURSE_FILE_SERVER_PATH
    with open(path+'captions.json', 'r+', encoding='utf-8') as JsonText:
        #JsonDate = json.dumps(JsonText.read(),ensure_ascii=False)
        JsonData = json.loads(JsonText.read())
        return render(request,'app/CaptionsEdit.html',{'temvarJsonData':JsonData,
                                                   'temvarVideoPath' :ServerPath+'LowBitrate.mp4'})
    return render(request,'app/CaptionsEdit.html')

#SlideEdit
def SlideEdit(request):
    assert isinstance(request, HttpRequest)
    #Login OP
    if request.user.is_authenticated() == False: 
        LoginStr = request.GET.get('link')
        if LoginStr:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
        else:
            return HttpResponseRedirect('/login')  
    #Login ED
    if (request.GET.get('ProjectNo')) :
        ProjectNo = request.GET.get('ProjectNo')
        course = models.course.objects.get(ProjectId=ProjectNo)
    elif (request.GET.get('id')) :
        id = request.GET.get('id')
        course = models.course.objects.get(CourseId=id)
    CourseId=course.CourseId
    path = COURSE_URL + CourseId[0:4] + '/' + CourseId + '/'
    FilePath = COURSE_ROOT + CourseId[0:4] + '/' + CourseId + '/'
    SlideName=''
    if course.SlideVersion is None or course.SlideVersion=='':
        SlideName=CourseId
    else:
        SlideName=CourseId+'_'+course.SlideVersion
    AbstractData=[]
    abstracts=models.CourseAbstract.objects.filter(course=course)
    if abstracts:
        for currentAbstract in abstracts:
            AbstractData.append({
                'index': currentAbstract.index, 
                'text': currentAbstract.Text
            })
    LecturerData=[]
    lecturers=models.lecturer.objects.filter(name=course.note)
    if lecturers:
        for  i in range(0, len(lecturers)):
            if lecturers[i].introduction:
                summary=lecturers[i].introduction
            else:    
                DOMTree = xml.dom.minidom.parse(LECTURER_ROOT+lecturers[i].IntroSrc)
                collection = DOMTree.documentElement
                summary=collection.getElementsByTagName("Information1")[0].firstChild.data
                summary=summary.replace("<![CDATA[","")
                summary=summary.replace("]]>","")
            LecturerData.append({
                'index':i,
                'id': lecturers[i].LecturerId, 
                'name': lecturers[i].name,
                'job':lecturers[i].post,
                'ImgSrc':'/LecturerFile/'+lecturers[i].PhotoSrc,
                'summary':summary
            })
    thislecturer=course.lecturer
    ThisLecturerData=[]
    if  thislecturer:
        ThisLecturerData.append({
                'id': thislecturer.LecturerId, 
                'name': thislecturer.name,
                'job':thislecturer.post,
                'ImgSrc':'/LecturerFile/'+thislecturer.PhotoSrc,
                'summary':thislecturer.introduction
            })
    with open(FilePath+'captions.json', 'r+', encoding='utf-8') as JsonText:
        #JsonDate = json.dumps(JsonText.read(),ensure_ascii=False)
        JsonData = json.loads(JsonText.read()) 
        return render(request,'app/SlideEdit.html',{'temvarCourseId':CourseId,
                                                   'temvarJsonData':JsonData,
                                                   'temvarDocPath' :'http://newpms.cei.cn/docs/p/PowerPointFrame.aspx?WOPISrc=http%3A%2F%2Fpmsdocs.cei.cn%3A666%2Fwopi%2Ffiles%2F'+SlideName+'.pptx%3Fuserid%3Dcc%26username%3Dchenchen&PowerPointView=EditView',
                                                   #'ModeNaviLink':'/CourseUpload/?id='+CourseId+'&ProjectNo='+ProjectNo,
                                                   'temvarCourseTitle':course.title,
                                                   #'ModeNaviTitle':'属性编辑',
                                                   'tempvarTextDownload':"http://newpms.cei.cn/fullTextDownload/?id="+CourseId,
                                                   'tempvarSlideDownload':path+'slide0.zip',
                                                   'tempvarCurrentSlideDownload':'/DocFile/'+SlideName+'.pptx',
                                                   'tempvarTestDownload':path+'test.zip',
                                                   'temvarAudioFilePath':path + CourseId +'.mp3',
                                                   #'temvarVideoFilePath':path+'rip.mp4',
                                                   'temvarJsonAbstractData':AbstractData,
                                                   'temvarJsonLecturerData':LecturerData,
                                                   'temvarThisLecturerData':ThisLecturerData,
                                                   'temvarKeyWords':course.KeyWords
                                                   })
    return render(request,'app/SlideEdit.html')

# VideoSegment
def VideoSegment(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        ret = {'status': False, 'data': None, 'error': None}
        try:
            id = request.POST.get('id')
            CourseThis = models.course.objects.get(CourseId=id)
            CourseThis.SegmentTime= request.POST.get('time')
            CourseThis.save()
            ret['status'] = True
            #TEST
            Tasks = models.EditTask.objects.filter(course=CourseThis)
            for ctask in Tasks:
                ctask.TaskState='2'
                ctask.save()
            #TEST
            #
            #NewTask = models.EditTask(course=CourseThis,TaskType='VideoSegment',TaskState='WaitingToBegin')
            NewTask = models.EditTask(TaskType='VideoSegment',TaskState='WaitingToBegin')
            NewTask.save()
            NewTask.course.add(CourseThis)
            NewTask.save()
            ret['data'] = 'DB_Success'
            #
        except Exception as e:
            ret['error'] = str(e)
        finally:   
            return HttpResponse(json.dumps(ret))
            #return HttpResponseRedirect('/TaskQuery')  
    else:
        id = request.GET.get('id')
        DataItems = models.course.objects.filter(CourseId=id)
        if DataItems[0].SegmentTime is None:
            SegmentTimeDisplay=''
        else:
            SegmentTimeDisplay=DataItems[0].SegmentTime
        return render(request, 'app/VideoSegment.html',{'InputValuleId':DataItems[0].CourseId,
                                                    'CourseTitle':DataItems[0].title,
                                                    'InputValuleSegmentTime':SegmentTimeDisplay})


#SrtUpload
@csrf_exempt 
def SrtUpload(request):  
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        ret = {'SRT': False, 'Data': False,'P-RET':False,}
        CourseId = request.POST.get('courseId')
        FileSrt = request.FILES.get('fileSrt')
        #
        path = COURSE_ROOT + CourseId[0:4] + '/' + CourseId + '/'
        if not os.path.exists(path):
            ret['SRT'] = 'Course path is not found'
        #情景：制作前资料 OP
        if (request.POST.get('mode')=='slide') and (os.path.splitext(FileSrt.name)[1] == '.zip'):
            DestinationFilePath = path + 'slide0'+os.path.splitext(FileSrt.name)[1]
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in FileSrt.chunks():
                DestinationFile.write(chunk)
            DestinationFile.close()
            ret['SRT'] = '上传成功'
            return HttpResponse(json.dumps(ret,ensure_ascii=False))    
        if (request.POST.get('mode')=='slide') and (os.path.splitext(FileSrt.name)[1] != '.zip'):
            ret['SRT'] = '只接收ZIP文件,请重新上传'
            return HttpResponse(json.dumps(ret,ensure_ascii=False))  
        #情景：制作前资料 ED
        if os.path.splitext(FileSrt.name)[1] != '.srt':
            ret['SRT'] = 'File is not SRT'
            return HttpResponse(json.dumps(ret))
        ThisTask=models.EditTask.objects.get(course=models.course.objects.get(CourseId=CourseId),TaskType='STT')
        if ThisTask.TaskState=='Finished':
            ret['SRT'] = '请不要反复上传，如需修改请线下联系'
            return HttpResponse(json.dumps(ret,ensure_ascii=False))
        #1
        DestinationFilePath = path + 'captions.srt'
        DestinationFile = open(DestinationFilePath, 'wb+')
        for chunk in FileSrt.chunks():
            DestinationFile.write(chunk)
        DestinationFile.close()
        #1-2
        srt_filename ='captions.srt'
        out_filename ='captions.json'
        srt = open(path + srt_filename, 'rb').read()
        if srt[:3] == codecs.BOM_UTF8:  
            srt = srt[3:]               
        srt = srt.decode('utf-8')       
        parsed_srt = JsonSuite.parse_srt(srt)
        open(path + out_filename, 'wb+').write(json.dumps(parsed_srt, indent=2, sort_keys=True,ensure_ascii=False).encode('utf8')) 
        ret['SRT'] = 'Success'
        #Data OP
        CurrentCourse = models.course.objects.get(CourseId=CourseId)
         #工单进度 OP
        ProjectRequest = requests.get(ProjectCollection_URL+"InterFace/Main.ashx?method=UpdateContentProgress&id="+CurrentCourse.ProjectId+"&progress=00000000-0000-0000-0000-000000000107")
        ret['P-RET'] = ProjectRequest.text
         #工单进度 ED
        CurrentCourse.progress= 'SrtUploaded'
        CurrentCourse.save()
        ThisTask.TaskState='Finished'
        ThisTask.FinishedDate=datetime.now()
        ThisTask.save()  
        ret['Data'] = '上传成功'
        #Data ED
        return HttpResponse(json.dumps(ret,ensure_ascii=False))
    else:
      mode  = request.GET.get('mode')
      if request.GET.get('id'):
          CourseId  = request.GET.get('id')
      else:     
          CourseId = models.course.objects.get(ProjectId=request.GET.get('ProjectNo')).CourseId
      CourseItems = models.course.objects.filter(CourseId=CourseId)
      return render(request, 'app/SrtUpload.html',{'CourseId':CourseId,
                                                    'CourseTitle':CourseItems[0].title,
                                                    'tempvarMode':mode,
                                                    })

#JsonTaskList
def JsonTaskList(request):
    assert isinstance(request, HttpRequest)
    #one
    #TaskItems = models.EditTask.objects.get()
    TaskItems = models.EditTask.objects.filter(TaskType='STT',TaskState='WaitingToEdit').values('id','course_id','course__title','CreateDate')
    #one
    #return HttpResponse(json.dumps(model_to_dict(TaskItems),default=JsonSuite.datetime_handler))
    #return HttpResponse(serializers.serialize("json",TaskItems))
    TaskList = list(TaskItems)
    return HttpResponse(json.dumps(TaskList,default=JsonSuite.datetime_handler,ensure_ascii=False))

#JsonCourseList
@csrf_exempt
def JsonCourseList(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        mode = request.POST.get('mode')
        if mode == 'edit':
            Items = models.course.objects.filter(SourceCourseId_id=None).values('ProjectId','title','lecturer__name','CreateDate','progress')
        CourseList = list(Items)
        return HttpResponse(json.dumps(CourseList,default=JsonSuite.datetime_handler,ensure_ascii=False))

# CourseUpload
def CourseUpload(request):
    #Login OP
    if request.user.is_authenticated() == False: 
        LoginStr = request.GET.get('link')
        if LoginStr:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
        else:
            return HttpResponseRedirect('/login')  
    #Login ED
    #
    if (request.GET.get('ProjectNo')) :
        ProjectNo = request.GET.get('ProjectNo')
        course = models.course.objects.get(ProjectId=ProjectNo)
        CourseId=course.CourseId
        ModeNaviLink= '/SlideEdit/?id='+CourseId+'&ProjectNo='+ProjectNo
    elif (request.GET.get('id')) :
        id = request.GET.get('id')
        course = models.course.objects.get(CourseId=id)
        CourseId=course.CourseId
        ModeNaviLink= '/SlideEdit/?id='+CourseId
    #
    #lecturer=course.lecturer
    #if lecturer is None: # lecturer.name : 'NoneType' object has no attribute 'name'
    #    return HttpResponse('请先添加讲师信息')
    ThisTitle=course.title
    if course.InternalCategory.first():
        ThisInternalCategory = course.InternalCategory.first()
        ThisInternalCategoryTop = course.InternalCategory.first().parent
        ThisInternalCategoryId = ThisInternalCategory.InternalCategoryId
        ThisInternalCategoryTopId = ThisInternalCategoryTop.InternalCategoryId
    else:
        ThisInternalCategoryId=''  
        ThisInternalCategoryTopId=''
    InternalCategoriesTop = models.InternalCategory.objects.filter(parent=None)
    InternalCategoriesLv2 = models.InternalCategory.objects.filter(~Q(parent=None))
    ThisDicCategoryList=course.PublishCategory.filter(type='guid')
    ThisDicIdList=[]
    for item in ThisDicCategoryList:
        ThisDicIdList.append(item.PublishCategoryId)
    ThisTYCategoryList=course.PublishCategory.filter(type='TYName')
    ThisTYIdList=[]
    for item in ThisTYCategoryList:
        ThisTYIdList.append(item.PublishCategoryId)
    ThisDZCategoryList=course.PublishCategory.filter(type='DZName')
    ThisDZIdList=[]
    for item in ThisDZCategoryList:
        ThisDZIdList.append(item.PublishCategoryId)
    ThisGXCategoryList=course.PublishCategory.filter(type='GXName')
    ThisGXIdList=[]
    for item in ThisGXCategoryList:
        ThisGXIdList.append(item.PublishCategoryId)
    e=course.EpisodeCount   
    episode=''          
    if e==2:
        episode ="（上）（下）"
    elif e==3:    
        episode ="（上）（中）（下）"
    elif e==4:
        episode ="（一）（二）（三）（四）"
    elif e==5:
        episode ="（一）（二）（三）（四）（五）"
    elif e==6:
        episode ="（一）（二）（三）（四）（五）（六）"
    elif e==7:
        episode ="（一）（二）（三）（四）（五）（六）（七）"
    elif e==8:
        episode ="（一）（二）（三）（四）（五）（六）（七）（八）"
    elif e==9:
        episode ="（一）（二）（三）（四）（五）（六）（七）（八）（九）"
    elif e==10:
        episode ="（一）（二）（三）（四）（五）（六）（七）（八）（九）（十）"                          
    return render(request, 'app/CourseUpload.html',{'temvarCourseId':course.CourseId,
                                                    'temvarCourseTitle':ThisTitle,
                                                    'temvarEpisode':episode,
                                                    'temvarGroupName':course.GroupName,
                                                    #'temvarKeyWords':course.KeyWords,
                                                    'temvarCourseProgress':course.progress,
                                                    #'temvarLecturerName':lecturer.name,
                                                    #'temvarLecturerPost':lecturer.post,
                                                    #'temvarLecturerIntro':lecturer.introduction,
                                                    #'temvarLecturerPic':"/LecturerFile/"+lecturer.PhotoSrc,
                                                    "temvarInternalCategoryId":ThisInternalCategoryId,
                                                    "temvarInternalCategoryIdTop":ThisInternalCategoryTopId,
                                                    'temvarInternalCategoryListTop':InternalCategoriesTop,
                                                    'temvarInternalCategoryListLv2': json.dumps(list(InternalCategoriesLv2.values())),
                                                    'temvarDicIdList':ThisDicIdList,
                                                    'temvarTYIdList':ThisTYIdList,
                                                    'temvarDZIdList':ThisDZIdList,
                                                    'temvarGXIdList':ThisGXIdList,
                                                    'ModeNaviLink':ModeNaviLink,
                                                    'ModeNaviTitle':'内容编辑'
                                                    })

# UpdateLecturer
def UpdateLecturer(request):
    if request.method == 'POST':
        ret = {'id': None, 'PicSrc': None}
        job=request.POST.get("LecturerJobInput")
        summary=request.POST.get("LecturerSummaryText")
        name=request.POST.get("LecturerNameInput")
        id=request.POST.get("id")
        if id:
            lecturer = models.lecturer.objects.get(LecturerId=id)
            lecturer.post = job
            lecturer.introduction = summary
            lecturer.save()
        else:
            id = datetime.now().strftime('%Y%m%d%H%M%S%f')  
            lecturer = models.lecturer(LecturerId=id,name=name,post=job,introduction=summary)
            lecturer.save()   
        ret['id']=lecturer.LecturerId
        file = request.FILES.get('LecturerPhotoInput')
        if file:
            if lecturer.PhotoSrc:
                os.remove(LECTURER_ROOT + lecturer.PhotoSrc)
            DestinationFilePath = LECTURER_ROOT + id + os.path.splitext(file.name)[1]
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in file.chunks():
                DestinationFile.write(chunk)
            DestinationFile.close()
            lecturer.PhotoSrc= id + os.path.splitext(file.name)[1]
            lecturer.save()
            ret['PicSrc']= LECTURER_URL + id + os.path.splitext(file.name)[1]
        else:
            ret['PicSrc']= LECTURER_URL + lecturer.PhotoSrc   
        CourseId=request.POST.get("CourseId")
        CourseThis = models.course.objects.get(CourseId=CourseId)
        CourseThis.lecturer=lecturer
        CourseThis.save()
        return HttpResponse(json.dumps(ret))

# UpdateCourseAbstract
def UpdateCourseAbstract(request):
    if request.method == 'POST':
        ret = {'res': None}
        ReqData=json.loads(request.body)
        id = ReqData['id']
        ReqAbstract=ReqData['AbstractText']
        ThisCourse = models.course.objects.get(CourseId=id)
        # keywords OP
        ReqKeywords = ReqData['KeyWords']
        ThisCourse.KeyWords=ReqKeywords
        ThisCourse.save()
        # keywords ED
        models.CourseAbstract.objects.filter(course=ThisCourse).delete()
        for i in ReqAbstract:
            text = i['text']
            CourseAbstract=models.CourseAbstract.objects.create(course=ThisCourse,index=ReqAbstract.index(i)+1,Text=text)
            CourseAbstract.save()
        ret['res']='success' 
        return HttpResponse(json.dumps(ret))

#SubCheck
def SubCheck(request):
    ret = {'res': None}
    if request.method == 'POST':
        ReqData=json.loads(request.body)
        id = ReqData['id']
        PageCount = ReqData['PageCount']
        ThisCourse = models.course.objects.get(CourseId=id)
        FilePath = COURSE_ROOT + id[0:4] + '/' + id + '/'
        with open(FilePath+'captions.json', 'r+', encoding='utf-8') as JsonText:
            JsonData = json.loads(JsonText.read()) 
            PrePage=0
            for subitem in JsonData:
                if subitem['type']=='SubItem':
                    if subitem['index']=='1' and subitem['PPTPagination']!='1':
                        ret['res']='请确认首条字幕关联第一页幻灯片' 
                        return HttpResponse(json.dumps(ret,ensure_ascii=False))  
                    if (subitem['PPTPagination']!='0') and (int(subitem['PPTPagination'])-PrePage==1):
                        PrePage+=1
                    elif (subitem['PPTPagination']!='0') and (int(subitem['PPTPagination'])-PrePage!=1): 
                        ret['res']='文稿上标注的幻灯片顺序可能不正确，存疑页码：'+ subitem['PPTPagination']
                        return HttpResponse(json.dumps(ret,ensure_ascii=False))    
                    else:
                        ret['res']='normal'
            if PageCount != 0 and PageCount != PrePage:
                ret['res']='请确保所有幻灯片('+ str(PageCount)+')都与文稿('+str(PrePage)+')关联'
                return HttpResponse(json.dumps(ret,ensure_ascii=False))
            ret['res']='pass'
    return HttpResponse(json.dumps(ret))    

# SaveTest
def SaveTestFile(request):
    if request.method == 'POST':
        ret = {'id': "None", 'Src': "None",'Text':""}
        ProjectNo=request.POST.get('ProjectNo')
        course = models.course.objects.get(ProjectId=ProjectNo)
        id=course.CourseId
        file = request.FILES.get('TestFileInput')
        if file and os.path.splitext(file.name)[1]=='.zip':
            DestinationFilePath = COURSE_ROOT + id[0:4] +"/" + id +"/"+"test"+ os.path.splitext(file.name)[1]
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in file.chunks():
                DestinationFile.write(chunk)
            DestinationFile.close()
            ret['Src']=COURSE_URL + id[0:4] +"/" + id +"/"+"test"+ os.path.splitext(file.name)[1]
            ret['Text']="成功"
        else:
            ret['Text']="只接受zip文件"
        return HttpResponse(json.dumps(ret))

# SlideUpload
def SlideUpload(request):
    if request.method == 'POST':
        ret = {'id': "None", 'Src': "None",'SlideVersion':"None"}
        ProjectNo=request.POST.get('ProjectNo')
        course = models.course.objects.get(ProjectId=ProjectNo)
        id=course.CourseId
        file = request.FILES.get('SlideUploadInput')
        if file and os.path.splitext(file.name)[1]=='.pptx':
            SlideVersion=0
            ret['SlideVersion']=course.SlideVersion
            if (course.SlideVersion is None) or (course.SlideVersion==''):
                SlideVersion=1
                #os.remove(DOC_ROOT + id + '.pptx')
            else:
                SlideVersion=int(course.SlideVersion)+1
                os.remove(DOC_ROOT + id +'_' + course.SlideVersion + '.pptx')
            course.SlideVersion=SlideVersion
            course.save() 
            DestinationFilePath = DOC_ROOT + id +'_' + str(SlideVersion) + os.path.splitext(file.name)[1]
            DestinationFile = open(DestinationFilePath, 'wb+')
            for chunk in file.chunks():
                DestinationFile.write(chunk)
            DestinationFile.close()

            ret['Src'] = id +'_' + str(SlideVersion)
        return HttpResponse(json.dumps(ret))    

# CourseMake
def CourseMake(request):
    assert isinstance(request, HttpRequest)
    #Login OP
    if request.user.is_authenticated():
        # Do something for authenticated users.
        CurrentUser=request.user.username
        DBUser=User.objects.get(username=CurrentUser) 
    else: 
        # Do something for anonymous users.
        LoginStr = request.GET.get('link')
        if CommonMethod.LinkLogin(LoginStr)!=False:
            user=CommonMethod.LinkLogin(LoginStr)
            login(request,user)
            DBUser=User.objects.get(username=user.username) 
        else:    
            return HttpResponseRedirect('/login')   
    #Login ED
    result = {"state":"None","note":"None"}
    if request.method == 'POST':
        mode=request.GET.get('mode')
        id=request.POST.get('courseId')
        ThisCourse = models.course.objects.get(CourseId=id)
        #info
        ThisCourse.title=request.POST.get('title')
        ThisCourse.GroupName=request.POST.get('groupName')
        #ThisCourse.KeyWords=request.POST.get('keyWords')
        #category
        ThisInternalCategoryId=request.POST.get('internalCategoryLevel2')
        InternalCategories=models.InternalCategory.objects.filter(InternalCategoryId=ThisInternalCategoryId)
        ThisCourse.InternalCategory.set(InternalCategories);
        ThisCourse.save()
        ThisCourse.PublishCategory.all().delete();
        DicJson=json.loads(request.POST.get('dicCategoryInput'))
        for item in DicJson:
            if models.PublishCategory.objects.filter(PublishCategoryId=item['id']).count()==0:
                NewCategory = models.PublishCategory.objects.create(PublishCategoryId=item['id'],type='guid',name=item['name'])
            ThisCourse.PublishCategory.add(models.PublishCategory.objects.get(PublishCategoryId=item['id']));
        TYJson=json.loads(request.POST.get('tyCategoryInput'))
        for item in TYJson:
            if models.PublishCategory.objects.filter(PublishCategoryId=item['id']).count()==0:
                NewCategory = models.PublishCategory.objects.create(PublishCategoryId=item['id'],type='TYName',name=item['name'])
            ThisCourse.PublishCategory.add(models.PublishCategory.objects.get(PublishCategoryId=item['id']));
        DZJson=json.loads(request.POST.get('dzCategoryInput'))
        for item in DZJson:
            if models.PublishCategory.objects.filter(PublishCategoryId=item['id']).count()==0:
                NewCategory = models.PublishCategory.objects.create(PublishCategoryId=item['id'],type='DZName',name=item['name'])
            ThisCourse.PublishCategory.add(models.PublishCategory.objects.get(PublishCategoryId=item['id']));
        GXJson=json.loads(request.POST.get('gxCategoryInput'))
        for item in GXJson:
            if models.PublishCategory.objects.filter(PublishCategoryId=item['id']).count()==0:
                NewCategory = models.PublishCategory.objects.create(PublishCategoryId=item['id'],type='GXName',name=item['name'])
            ThisCourse.PublishCategory.add(models.PublishCategory.objects.get(PublishCategoryId=item['id']));    
        ThisCourse.save()
        result["state"]='成功'
        result["note"]=ThisInternalCategoryId
        #
        if mode=='pass':
            #shutil.copyfile(DOC_ROOT+id+'.pptx', COURSE_ROOT + id[0:4] + '/' + id + '/slide.pptx') 
            ThisCourse = models.course.objects.get(CourseId=id)
            #Copy Slide OP
            if (ThisCourse.SlideVersion is None) or (ThisCourse.SlideVersion==''):
                #shutil.copyfile可替换
                shutil.copyfile(DOC_ROOT+id+'.pptx', COURSE_ROOT + id[0:4] + '/' + id + '/slide.pptx') 
            else:
                shutil.copyfile(DOC_ROOT + id +'_' + ThisCourse.SlideVersion + '.pptx', COURSE_ROOT + id[0:4] + '/' + id + '/slide.pptx') 
            #Copy Slide ED    
            if (models.EditTask.objects.filter(course=ThisCourse,TaskType='CourseMake',TaskState='creating').count()>0):
                result["state"]='请不要重复添加任务'
            else:
                #NewTask = models.EditTask(course=ThisCourse,TaskType='CourseMake',TaskState='WaitingToBegin')
                # make
                NewTask = models.EditTask(TaskType='CourseMake',TaskState='WaitingToBegin',creator=DBUser)
                NewTask.save()
                NewTask.course.add(ThisCourse)
                NewTask.TaskState='WaitingToBegin'
                NewTask.save()
                # pub
                NewPubTask = models.EditTask(TaskType='CourseFtpPublish',TaskState='creating',creator=DBUser)
                NewPubTask.save()
                NewPubTask.course.add(ThisCourse)
                NewPubTask.TaskState='WaitingToBegin'
                NewPubTask.save()
                result["state"]='成功加入制作队列'
    return HttpResponse(json.dumps(result,ensure_ascii=False))

# FullTextDownloadTXT
def FullTextDownloadTXT(request):
    assert isinstance(request, HttpRequest)
    id = request.GET.get('id')
    ThisCourse = models.course.objects.get(CourseId=id)
    path = COURSE_ROOT + id[0:4] + '/' + id + '/data/'
    with open(path+'captions.json', 'r+', encoding='utf-8') as JsonText:
        JsonContent = JsonText.read()
        if JsonContent.startswith(u'\ufeff'):
            JsonContent = JsonContent.encode('utf8')[3:].decode('utf8')
        JsonData = json.loads(JsonContent)
        txtName = "FullText.txt"
        f=open(path+txtName, "w",encoding='utf-8')
        for item in JsonData:
            if item['type'].startswith('TitleItem') :
                f.write('\r\n' + '\r\n' + '      ' + item['content']+ '\r\n')
            elif item['type']=='SubItem':
                if item['IsBeginningOfParagraph'] == 'false' :
                    f.write(item['content'])
                else:
                    f.write('\r\n'+ '      ' +item['content'])
        f.close()
    file=open(path + 'FullText.txt','rb')      
    response =FileResponse(file)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="'+ id +'.txt"'  
    return response     

# FullTextDownload From Srt
def FullTextDownloadFromSrt(request):
    assert isinstance(request, HttpRequest)
    id = request.GET.get('id')
    ThisCourse = models.course.objects.get(CourseId=id)
    path = COURSE_ROOT + id[0:4] + '/' + id + '/'
    srt = open(path + 'captions.srt', 'rb').read()
    if srt[:3] == codecs.BOM_UTF8:  
        srt = srt[3:]               
    srt = srt.decode('utf-8')       
    parsed_srt = JsonSuite.srtToTxt(srt)
    txtName = "FullTextFromSrt.txt"
    f=open(path+txtName, "w",encoding='utf-8')
    f.write(parsed_srt)
    f.close()
    file=open(path + 'FullTextFromSrt.txt','rb')      
    response =FileResponse(file)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="'+ id +'.txt"'  
    return response  

# JsonDataSave
def JsonDataSave(request):
    assert isinstance(request, HttpRequest)
    ret = {'status': False, 'data': None, 'error': None}
    if request.method == 'POST':
            mode = request.GET.get('mode')
            CourseId=request.GET.get('id')
            if mode=='auto':
                TargetFile='captions_auto.json'
            else:
                TargetFile='captions.json'
            path = os.path.join(COURSE_ROOT, CourseId[0:4] + '/' + CourseId + '/')
            #JsonData =  json.dumps(request.body, indent=2, sort_keys=True,ensure_ascii=False).encode('utf8')
            JsonData=str(request.body, encoding = "utf-8")
            #
            e=1
            JsonObj = json.loads(JsonData)
            for i in JsonObj:
                if i["type"]=="SubItem" and i["IsBeginningOfParagraph"]=="episode":
                    e += 1  
            course = models.course.objects.get(CourseId=CourseId)   
            course.EpisodeCount=e
            course.save()    
            #
            #ret['data'] = request.body
            f = open(path+TargetFile,'w',encoding= 'utf8') #打开文件open()是file()的别名
            f.write(JsonData) #把字符串写入文件
            f.close() #关闭文件
            ret['status'] = True                   
            #
            return HttpResponse()
    else:
        return JsonResponse(ret) 

# JsonDataRestore 
def JsonDataRestore(request):
    assert isinstance(request, HttpRequest)
    ret = {'status': False, 'data': None, 'error': None}
    if request.method == 'POST':
            path = os.path.join(COURSE_FILE_PATH, 'temp/')
            if os.path.exists(path + 'captions_auto.json'):
                srt = open(path + 'captions_auto.json', 'rb').read()
                if srt[:3] == codecs.BOM_UTF8:  
                    srt = srt[3:]               
                srt = srt.decode('utf-8')  
                f = open(path+'captions.json','w',encoding= 'utf8') #打开文件open()是file()的别名
                f.write(srt) #把字符串写入文件
                f.close() #关闭文件
                ret['status'] = True                   
            else:
                ret['status'] = 'no file'   
            return HttpResponse(ret)
    else:
        return JsonResponse(ret) 

# JsonCourseAbstractUpdate
def JsonCourseAbstractUpdate(request):
    assert isinstance(request, HttpRequest)
    ret = {'status': False, 'data': None, 'error': None}
    if request.method == 'POST':
            JsonData= json.loads(request.body)
            id = JsonData['id']
            CourseThis = models.course.objects.get(CourseId=id)
            CourseThis.AbstractText= JsonData['AbstractText']
            CourseThis.save()              
            #
            return HttpResponse(ret)
    else:
        return JsonResponse(ret) 

# Old Course
def OldCourseQuery(request):
    #
    ThisHeaders={'Access-Control-Allow-Origin':'*'}
    #
    assert isinstance(request, HttpRequest)
    #request.encoding='gb2312'
    QueryTitle =''
    if request.GET.get('title') :
        QueryTitle = urllib.parse.unquote(request.GET.get('title'))
    QueryLecturer =''
    if request.GET.get('lecturer') :  
        QueryLecturer = urllib.parse.unquote(request.GET.get('lecturer'))   
    QueryKey = ''    
    if request.GET.get('key') :
        QueryKey = urllib.parse.unquote(request.GET.get('key'))
    QueryType = ''
    if request.GET.get('type') :
        QueryType = urllib.parse.unquote(request.GET.get('type'))
    QuerySource = ''
    if request.GET.get('source') :
        QuerySource = urllib.parse.unquote(request.GET.get('source'))    
        if  QuerySource =='1' :
             QuerySource='客户'
        else:
            QuerySource = ''
    list = [] # 空列表
    # 打开数据库连接 
    db = pymysql.connect("203.207.118.110","root","cuijingyi","zjsp",charset='utf8') 
    # 使用cursor()方法获取操作游标  
    cursor = db.cursor() 
    # SQL 查询语句 
    sql = "SELECT Id ,Theme,Themegroup,Speaker,Speakerinfo,Format,Date,'旧课件' as DataType,Sourse,Producer,Mark,Duration FROM course where Theme like '%" \
    + QueryTitle + "%' and Speaker like '%" + QueryLecturer + "%' and KeyWords like '%" + QueryKey + "%' and Sourse like '%" + QuerySource +"%' and Format like '%" + QueryType + "%' order by Date desc,Theme asc"
    #return HttpResponse(sql)
    try: 
    # 执行SQL语句 
        cursor.execute(sql) 
        # 获取所有记录列表 
        results = cursor.fetchall() 
        for row in results: 
            CourseId = str(row[0])
            title = str(row[1]) 
            GroupName = str(row[2]) 
            lecturer = str(row[3]) 
            post = str(row[4]) 
            TempletType = str(row[5])
            Date = str(row[6])
            DataType = str(row[7])
            type = str(row[8])
            creator = str(row[9])
            if str(row[10])=='10000' :
                progress='未审未发'
            elif str(row[10])=='11000' :
                 progress='已审未发'   
            elif str(row[10])=='10010' :
                 progress='未审已发'    
            elif str(row[10])=='11010' :
                 progress='已审已发'   
            duration = str(row[11])         
            dict = {}
            dict = {'CourseId': CourseId, 'title': title,'GroupName':GroupName, 'lecturer_name': lecturer,'post':post, 'TempletType': TempletType, 'CreateDate': Date,'DataType':DataType,'type':type,'creator':creator,'progress':progress,'duration':duration}
            list.append(dict)
    except: 
        print ("Error: unable to fetch data") 
    # 关闭数据库连接 
    db.close() 
    #return JsonResponse(json.dumps(list,ensure_ascii=False)) 
    return HttpResponse(json.dumps(list,ensure_ascii=False))
# Old Course Exacted
def OldCourseQueryExacted(request):
    #
    ThisHeaders={'Access-Control-Allow-Origin':'*'}
    #
    assert isinstance(request, HttpRequest)
    QueryField =''
    if request.GET.get('field') :
        QueryField = urllib.parse.unquote(request.GET.get('field'))
    QueryVal =''
    if request.GET.get('val') :  
        QueryVal = urllib.parse.unquote(request.GET.get('val'))   
    SQLField =''
    if QueryField=='id' :
        SQLField ='Id'
    elif QueryField=='title' :
         SQLField ='Theme'
    list = [] # 空列表
    # 打开数据库连接 
    db = pymysql.connect("203.207.118.110","root","cuijingyi","zjsp",charset='utf8') 
    # 使用cursor()方法获取操作游标  
    cursor = db.cursor() 
    # SQL 查询语句 
    sql = "SELECT Id,Theme,Themegroup,Speaker,Speakerinfo,Format,Date,'旧课件' as DataType,Sourse,Producer as creator,Duration as duration,Mark,Duration FROM course where " + SQLField + " = '"  + QueryVal + "' order by Date desc,Theme asc limit 1"
    #return HttpResponse(sql)
    try: 
    # 执行SQL语句 
        cursor.execute(sql) 
        # 获取所有记录列表 
        results = cursor.fetchall() 
        for row in results: 
            CourseId = str(row[0])
            title = str(row[1]) 
            GroupName = str(row[2]) 
            lecturer = str(row[3]) 
            post = str(row[4]) 
            TempletType = str(row[5])
            Date = str(row[6])
            DataType = str(row[7])
            type = str(row[8])
            creator = str(row[9])
            if str(row[10])=='10000' :
                progress='未审未发'
            elif str(row[10])=='11000' :
                 progress='已审未发'   
            elif str(row[10])=='10010' :
                 progress='未审已发'    
            elif str(row[10])=='11010' :
                 progress='已审已发'   
            duration = str(row[11])           
            dict = {}
            dict = {'CourseId': CourseId, 'title': title,'GroupName':GroupName, 'lecturer_name': lecturer,'post':post, 'TempletType': TempletType, 'CreateDate': Date,'DataType':DataType,'type':type,'creator':creator,'progress':progress,'duration':duration}
            list.append(dict)
    except: 
        print ("Error: unable to fetch data") 
    # 关闭数据库连接 
    db.close() 
    return HttpResponse(json.dumps(list,ensure_ascii=False))

#JsonLogin
@csrf_exempt
def JsonLogin(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        PassWord = request.POST.get('PassWord')
    ret = {'status': False,'FirstName':'','LastName':''}
    user = authenticate(username=UserName,password=PassWord)
    if user:
        ret['status'] = True
        ret['FirstName'] = user.first_name
        ret['LastName'] = user.last_name
        login(request, user)
    else:
        ret['status'] = False
    #return HttpResponse(json.dumps(ret))
    response = HttpResponse(json.dumps(ret))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "x-csrftoken"
    return response

# Login OP
@csrf_exempt
def ApiLogin(request):
    ret = {'status': False,'username':'','group':'','FirstName':'','LastName':''}
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        # Django提供的authenticate函数，验证用户名和密码是否在数据库中匹配
        user = authenticate(username=username, password=password)
        if user is not None:
            # Django提供的login函数，将当前登录用户信息保存到会话key中
            #login(request, user)
            # 进行登录成功的操作，重定向到某处等
            ret['status'] = True
            ret['username'] = user.username
            ret['group'] = user.groups.first().name
            ret['FirstName'] = user.first_name
            ret['LastName'] = user.last_name
        else:
            # 返回用户名和密码错误信息
            ret['status'] = username+password
    else:
        ret['status'] = False
    #    
    response = HttpResponse(json.dumps(ret))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "x-csrftoken"
    return response
# Login ED

# REST OP
class CourseViewSet(viewsets.ModelViewSet): 
    serializer_class = RestSerializers.CourseSerializer  
    #permission_classes = (permissions.IsAuthenticated,) #,结尾必须有
    queryset = models.course.objects.all()
    @list_route() # 不写 404找不到网页
    def test(self, request): 
        #
        ThisHeaders={'Access-Control-Allow-Origin':'*'}
        #
        values = request.META.items()
        html = []
        for k, v in values:
            html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
        return HttpResponse('<table>%s</table>' % '\n'.join(html))
        #return Response(content_range,headers=ThisHeaders)
    @list_route()    
    def finished(self, request): #未发布 
        #
        ThisHeaders={'Access-Control-Allow-Origin':'*'}
        #
        courses = models.course.objects.filter((~Q(SourceCourseId=None) & Q(progress=None)) | Q(EpisodeCount=1,progress='made')) 
        serializer = RestSerializers.CourseSerializer(courses, many=True) 
        return Response(serializer.data,headers=ThisHeaders)
    @list_route()
    def FieldQuery(self, request): 
        #
        ThisHeaders={'Access-Control-Allow-Origin':'*'}
        #
        keyword=''
        if request.GET.get('key') :
            keyword = request.GET.get('key') # 获取参数
        title=''
        if request.GET.get('title') :
            title=request.GET.get('title')
        lecturer='' 
        if request.GET.get('lecturer') :
            lecturer=request.GET.get('lecturer')
        TempletType = ''    
        if request.GET.get('type') :
            TempletType=request.GET.get('type')
            if TempletType=='三分屏' :
                TempletType='slide'
            elif TempletType=='单视频' :
                TempletType='X'
            elif TempletType=='微课' :
                TempletType='Y'    
        SourceType='' 
        if request.GET.get('source') :
            SourceType=request.GET.get('source')
            if SourceType=='1' :
                SourceType = 'X'
        courses = models.course.objects.filter((~Q(SourceCourseId=None) | Q(EpisodeCount=1,progress='made')) & (Q(title__contains=title) & Q(KeyWords__contains=keyword) & Q(lecturer__name__contains=lecturer) & Q(type__contains=SourceType) & Q(TempletType__contains=TempletType)))
        #courses = models.course.objects.filter((~Q(SourceCourseId=None) & Q(SourceCourseId__lecturer__name__contains=keyword)) | (Q(EpisodeCount=1,progress='made') & Q(lecturer__name__contains=keyword)))
        serializer = RestSerializers.CourseSerializer(courses, many=True) 
        return Response(serializer.data,headers=ThisHeaders) # 最后返回经过序列化的数据 
    @list_route()
    def FieldQueryExacted(self, request): 
        #
        ThisHeaders={'Access-Control-Allow-Origin':'*'}
        #
        field=''
        if request.GET.get('field') :
            field = request.GET.get('field') # 获取参数
        val=''
        if request.GET.get('val') :
            val = request.GET.get('val')
        if field == 'title' :
            courses = models.course.objects.filter(title=val)
        elif field == 'id' :   
            courses = models.course.objects.filter(CourseId=val)
        serializer = RestSerializers.CourseSerializer(courses, many=True) 
        return Response(serializer.data,headers=ThisHeaders) # 最后返回经过序列化的数据 
    # function based OP
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def EditTask_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        EditTasks = models.EditTask.objects.all()
        serializer = RestSerializers.EditTaskSerializer(EditTasks, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.get(username=data['creator'])
        if user:
            data['creator'] = int(user.id) #  不转换  Expected pk value, received str.
        else:
            return JSONResponse("None User", status=400)
        serializer = RestSerializers.EditTaskSerializer(data=data)
        if serializer.is_valid():
            CourseId = data['course'][0]
            ThisCourse = models.course.objects.filter(CourseId=CourseId)
            if (models.EditTask.objects.filter(course=ThisCourse,TaskType='CourseFtpPublish',TaskState='WaitingToBegin').count()>0) :
                return JSONResponse("Task Repetition", status=423)     
            else:
                serializer.save()
                return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    # function based ED
    # class based OP
class EditTaskList(APIView):
    permission_classes = (permissions.IsAuthenticated,) #,结尾必须有
    #authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    def get(self, request, format=None):
        EditTasks = models.EditTask.objects.all()
        serializer = RestSerializers.EditTaskSerializer(EditTasks, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        token = request.META['HTTP_AUTHORIZATION']
        token = token.replace("JWT ", "")
        UserInfo = jwt_decode_handler(token)
        data['creator'] = int(UserInfo['user_id'])
        #user = User.objects.get(username=data['creator'])
        #if user:
        #    data['creator'] = int(user.id) #  不转换  Expected pk value, received str.
        #else:
        #    return JSONResponse("None User", status=400)
        data['TaskState'] = 'WaitingToBegin'
        serializer = RestSerializers.EditTaskSerializer(data=data)
        if serializer.is_valid():
            CourseId = data['course'][0]
            ThisCourse = models.course.objects.filter(CourseId=CourseId)
            if (models.EditTask.objects.filter(course=ThisCourse,TaskType=data['TaskType'],TaskState='WaitingToBegin').count()>0) and (data['TaskType']!='CourseDownload'):
                return Response("Task Repetition", status=status.HTTP_204_NO_CONTENT)     
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseTempletList(APIView):
    #permission_classes = (permissions.IsAuthenticated,) #,结尾必须有
    def get(self, request, format=None):
        CourseTemplets = models.CourseTemplet.objects.all()
        serializer = RestSerializers.CourseTempletSerializer(CourseTemplets, many=True)
        return Response(serializer.data)
# REST ED
    
