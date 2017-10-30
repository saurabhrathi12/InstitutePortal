# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
import MySQLdb
import datetime

# Create your views here.

db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
cur=db.cursor()

def mlogin(request):
	if request.session.has_key("admin"):
		return redirect("dashboard")
	request.session["admin"]=True
	username=request.POST.get('username')
	password=request.POST.get('password')
	print username,password
	if username and password:
		if username == "admin":
			if password == "password":
				return redirect("dashboard")
	return render(request,'management/mlogin.html')


def dashboard(request):
	if not request.session.has_key("admin"):
		return redirect("mlogin")
	contextdata={}

	query="SELECT * FROM student"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['student']=ans

	query="SELECT * FROM teacher"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['teacher']=ans

	query="SELECT * FROM classroom"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['classroom']=ans

	query="SELECT batch_id,standard,subject,name,name,hall_name,fee FROM batch natural join teacher natural join classroom"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['batch']=ans

	query="SELECT * FROM time_slot"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['time_slot']=ans
	

	return render(request,'management/dashboard.html',contextdata)

def deletestudent(request,pk):
	query="DELETE FROM student WHERE student_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deleteteacher(request,pk):
	query="DELETE FROM teacher WHERE teacher_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deleteclassroom(request,pk):
	query="DELETE FROM classroom WHERE classroom_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletebatch(request,pk):
	query="DELETE FROM batch WHERE batch_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def mlogout(request):
	if request.session.has_key("admin"):
		del request.session["admin"]
	return redirect("mlogin")