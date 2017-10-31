from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^mlogin$', views.mlogin, name='mlogin'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^deletestudent/(?P<pk>\d+)/$', views.deletestudent, name='deletestudent'),
	url(r'^deleteteacher/(?P<pk>\d+)/$', views.deleteteacher, name='deleteteacher'),
	url(r'^deleteclassroom/(?P<pk>\d+)/$', views.deleteclassroom, name='deleteclassroom'),
	url(r'^deletebatch/(?P<pk>\d+)/$', views.deletebatch, name='deletebatch'),
	url(r'^deletejoins/(?P<pk>\d+)/(?P<qk>\d+)/$', views.deletejoins, name='deletejoins'),
	url(r'^deletebatchtimeslot/(?P<pk>\d+)/(?P<qk>\d+)/$', views.deletebatchtimeslot, name='deletebatchtimeslot'),
	url(r'^deleteattendance/(?P<pk>\d+)/(?P<qk>\d+)/(?P<rk>[-\d]+)/$', views.deleteattendance, name='deleteattendance'),
	url(r'^deletefee/(?P<pk>\d+)/$', views.deletefee, name='deletefee'),
	url(r'^deletecomment/(?P<pk>\d+)/$', views.deletecomment, name='deletecomment'),
	url(r'^mlogout$', views.mlogout, name='mlogout'),
]