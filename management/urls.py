from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^mlogin$', views.mlogin, name='mlogin'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^deletestudent/(?P<pk>\d+)/$', views.deletestudent, name='deletestudent'),
	url(r'^deleteteacher/(?P<pk>\d+)/$', views.deleteteacher, name='deleteteacher'),
	url(r'^deleteclassroom/(?P<pk>\d+)/$', views.deleteclassroom, name='deleteclassroom'),
	url(r'^deletebatch/(?P<pk>\d+)/$', views.deletebatch, name='deletebatch'),
#	url(r'^student_fee/(?P<pk>\d+)/$', views.student_fee, name='student_fee'),
#	url(r'^teacher_dashboard$', views.teacher_dashboard, name='teacher_dashboard'),
#	url(r'^teacher_attendance/(?P<pk>\d+)/$', views.teacher_attendance, name='teacher_attendance'),
#	url(r'^teacher_fee/(?P<pk>\d+)/$', views.teacher_fee, name='teacher_fee'),
#	url(r'^discussion/(?P<pk>\d+)/$', views.discussion, name='discussion'),
	url(r'^mlogout$', views.mlogout, name='mlogout'),
]