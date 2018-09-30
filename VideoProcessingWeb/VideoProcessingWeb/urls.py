"""
Definition of urls for VideoProcessingWeb.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
admin.autodiscover()

#REST OP
from rest_framework.routers import DefaultRouter
from app.views import CourseViewSet
RestRouter = DefaultRouter()
RestRouter.register(r'course', app.views.CourseViewSet)
#REST ED


urlpatterns = [
    # Examples:
    #url(r'^$', app.views.home, name='home'),
    url(r'^$', app.views.MyTask, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', django.contrib.auth.views.LoginView.as_view(template_name='app/login.html'), name='login'),
    url(r'^logout$', django.contrib.auth.views.LogoutView.as_view(next_page='/'), name='logout'),
    #url(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': app.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    #url(r'^logout$',
    #    django.contrib.auth.views.logout,
    #    {
    #        'next_page': '/',
    #    },
    #    name='logout'), 

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),

    url(r'^VideoUpload',app.views.VideoUpload,name='Route_VideoUpload'),
    url(r'^FTPVideoUpload/$',app.views.FTPVideoUpload,name='Route_FTPVideoUpload'),
    url(r'^PlayVideo',app.views.PlayVideo,name='Route_PlayVideo'),
    url(r'^AjaxVideoUploadPage/$', app.views.AjaxVideoUploadPage,name='Route_AjaxVideoUploadPage'),  
    url(r'^AjaxVideoUpload/$', app.views.AjaxVideoUpload,name='Route_AjaxVideoUpload'),
    url(r'^TaskQuery',app.views.TaskQuery,name='Route_TaskQuery'),
    url(r'^MyTask',app.views.MyTask,name='Route_MyTask'),
    url(r'^STTEditList',app.views.STTEditList,name='Route_STTEditList'),
    url(r'^STTEdit/$',app.views.STTEdit,name='Route_STTEdit'),
    url(r'^CaptionsEdit/$',app.views.CaptionsEdit,name='Route_CaptionsEdit'),
    url(r'^SlideEdit/$',app.views.SlideEdit,name='Route_SlideEdit'),
    url(r'^VideoSegmentList',app.views.VideoSegmentList,name='Route_VideoSegmentList'),
    url(r'^VideoSegment$',app.views.VideoSegment,name='Route_VideoSegment'),
    url(r'^VideoSegment/$',app.views.VideoSegment,name='Route_VideoSegment'),
    url(r'^SrtUpload/$',app.views.SrtUpload,name='Route_SrtUpload'),
    url(r'^CourseUpload',app.views.CourseUpload,name='Route_CourseUpload'),
    url(r'^UpdateLecturer/$',app.views.UpdateLecturer,name='Route_UpdateLecturer'),
    url(r'^SaveTestFile/$',app.views.SaveTestFile,name='Route_SaveTestFile'),
    url(r'^SlideUpload/$',app.views.SlideUpload,name='Route_SlideUpload'),
    url(r'^CourseMake/$',app.views.CourseMake,name='Route_CourseMake'),
    url(r'^UpdateCourseAbstract/$',app.views.UpdateCourseAbstract,name='Route_UpdateCourseAbstract'),
    url(r'^CourseQuery/$',app.views.CourseQuery,name='Route_CourseQuery'),
    url(r'^CourseHandle/$',app.views.CourseHandle,name='Route_CourseHandle'),
    url(r'^SubCheck/$',app.views.SubCheck,name='Route_SubCheck'),
    url(r'^FullTextDownloadTXT/$',app.views.FullTextDownloadTXT,name='Route_FullTextDownloadTXT'),
    url(r'^FullTextDownloadFromSrt/$',app.views.FullTextDownloadFromSrt,name='Route_FullTextDownloadFromSrt'),
    url(r'^SRTDownload/$',app.views.SRTDownload,name='Route_SRTDownload'),
    #
    url(r'^JsonLogin/$',app.views.JsonLogin,name='Route_JsonLogin'),
    url(r'^JsonTaskList/$',app.views.JsonTaskList,name='Route_JsonTaskList'),
    url(r'^JsonCourseList/$',app.views.JsonCourseList,name='Route_JsonCourseList'),
    url(r'^JsonDataSave/$',app.views.JsonDataSave,name='Route_JsonDataSave'),
    url(r'^JsonDataRestore/$',app.views.JsonDataRestore,name='Route_JsonDataRestore'),
    url(r'^JsonCourseAbstractUpdate/$',app.views.JsonCourseAbstractUpdate,name='Route_JsonCourseAbstractUpdate'),
    url(r'^OldCourseQuery/$',app.views.OldCourseQuery,name='Route_OldCourseQuery'),
    url(r'^OldCourseQueryExacted/$',app.views.OldCourseQueryExacted,name='Route_OldCourseQueryExacted'),
    url(r'^ApiLogin/$',app.views.ApiLogin,name='Route_ApiLogin'),
    #REST
    #url(r'^', include(RestRouter.urls)),
    url(r'^', include(RestRouter.urls)),
    #url(r'^edittask/$', app.views.EditTask_list),
    #url(r'^edittask/(?P<userid>[\s\S]*)/$', app.views.EditTaskList.as_view()),
    url(r'^edittask/$', app.views.EditTaskList.as_view()),
    url(r'^edittaskdetail/$', app.views.EditTaskDetail.as_view()),
    url(r'^coursetemplet/$', app.views.CourseTempletList.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + static(settings.COURSE_URL,document_root=settings.COURSE_ROOT)
