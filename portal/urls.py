from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
	url(r'^student_dashboard$', views.student_dashboard, name='student_dashboard'),
	url(r'^student_attendance/(?P<pk>\d+)/$', views.student_attendance, name='student_attendance'),
	url(r'^student_fee/(?P<pk>\d+)/$', views.student_fee, name='student_fee'),
	url(r'^teacher_dashboard$', views.teacher_dashboard, name='teacher_dashboard'),
	url(r'^teacher_attendance/(?P<pk>\d+)/$', views.teacher_attendance, name='teacher_attendance'),
	url(r'^teacher_fee/(?P<pk>\d+)/$', views.teacher_fee, name='teacher_fee'),
	url(r'^discussion/(?P<pk>\d+)/$', views.discussion, name='discussion'),
	url(r'^logout$', views.logout, name='logout'),
]