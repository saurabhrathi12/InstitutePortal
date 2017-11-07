from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import MySQLdb
import datetime
import hashlib
def connect():
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	#db=MySQLdb.connect(host="rathiclasses.mysql.pythonanywhere-services.com",user="rathiclasses",passwd="qwerty123",db="rathiclasses$institute")
	cur=db.cursor()
	return db,cur

def mlogin(request):
	if request.session.has_key("admin"):
		return redirect("dashboard")
	username=request.POST.get('username')
	password=request.POST.get('password')
	if username and password:
		if username == "admin":
			if password == "password":
				request.session["admin"]="admin"
				messages.success(request,"Successful Login")
				return redirect("dashboard")
		messages.error(request,"Wrong username and/or password")
	return render(request,'management/mlogin.html')


def dashboard(request):
	db,cur=connect()
	if not request.session.has_key("admin"):
		return redirect("mlogin")
	contextdata={}

	name=request.POST.get('name')
	standard=request.POST.get('standard')
	school=request.POST.get('school')
	dateofbirth=request.POST.get('dateofbirth')
	father_name=request.POST.get('father_name')
	mother_name=request.POST.get('mother_name')
	mobile=request.POST.get('mobile')
	address=request.POST.get('address')	
	if name and standard and school and father_name and mother_name and mobile and address and dateofbirth:
		standard=int(standard)
		query="insert into student(name,mobile,dateofbirth,address,father_name,mother_name,standard,school) values('%s','%s','%s','%s','%s','%s','%d','%s')"%(name,mobile,dateofbirth,address,father_name,mother_name,standard,school)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	student_id=request.POST.get('ustudentid')
	name=request.POST.get('uname')
	standard=request.POST.get('ustandard')
	school=request.POST.get('uschool')
	dateofbirth=request.POST.get('udateofbirth')
	father_name=request.POST.get('ufather_name')
	mother_name=request.POST.get('umother_name')
	mobile=request.POST.get('umobile')
	address=request.POST.get('uaddress')
	if student_id and name and standard and school and father_name and mother_name and mobile and address and dateofbirth:
		student_id=int(student_id)
		standard=int(standard)
		query="update student set name = '%s', standard='%d', school='%s', dateofbirth='%s',father_name='%s',mother_name='%s',mobile='%s',address='%s' where student_id='%d' "%(name,standard,school,dateofbirth,father_name,mother_name,mobile,address,student_id)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully updated")
		except:
			messages.error(request,"Enter correct values")


	password=request.POST.get('password2')
	name=request.POST.get('name2')
	mobile=request.POST.get('mobile2')
	date=request.POST.get('dateofbirth2')
	address=request.POST.get('address2')
	if password and name and mobile and date and address:
		password=hashlib.sha512(password).hexdigest()
		date=datetime.datetime.strptime(date, '%Y-%m-%d').date()
		query="insert into teacher(password, name, mobile, dateofbirth, address) values('%s','%s','%s','%s','%s')"%(password,name,mobile,date,address)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	teacher_id=request.POST.get('utid')
	name=request.POST.get('uname2')
	mobile=request.POST.get('umobile2')
	date=request.POST.get('udateofbirth2')
	address=request.POST.get('uaddress2')
	if teacher_id and name and mobile and date and address:
		teacher_id=int(teacher_id)
		date=datetime.datetime.strptime(date, '%Y-%m-%d').date()
		query="update teacher set name='%s', mobile='%s', dateofbirth='%s', address='%s' where teacher_id='%d' "%(name,mobile,date,address,teacher_id)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully updated")
		except:
			messages.error(request,"Enter correct values")

	name=request.POST.get('name3')
	capacity=request.POST.get('capacity3')
	if name and capacity:
		query="insert into classroom(hall_name,capacity) values('%s','%d')"%(name,int(capacity))
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	standard=request.POST.get('standard4')
	subject=request.POST.get('subject4')
	fee=request.POST.get('fee4')
	teacher_id=request.POST.get('teacherid4')
	room_id=request.POST.get('roomid4')
	if standard and subject and fee and teacher_id and room_id:
		query="insert into batch(standard, subject, teacher_id, room_id, fee) values('%d', '%s', '%d', '%d', '%d')"%(int(standard), subject, int(teacher_id), int(room_id), int(fee)) 
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	day=request.POST.get('day5')
	start_time=request.POST.get('start5')
	end_time=request.POST.get('end5')
	if day and start_time and end_time:
		start_time=float(start_time)
		end_time=float(end_time)
		query="insert into time_slot(day, start_time, end_time) values('%s','%f','%f')"%(day, start_time, end_time)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	student_id=request.POST.get('studentid6')
	batch_id=request.POST.get('batchid6')
	fee=request.POST.get('fee6')
	if student_id and batch_id and fee:
		student_id=int(student_id)
		batch_id=int(batch_id)
		fee=int(fee)
		try:
			query="insert into joins(student_id, batch_id) values('%d','%d')"%(student_id,batch_id)
			cur.execute(query)
			query="INSERT into fee(amount,dateofdeposit,student_id,batch_id) values('%d',curdate(),'%d','%d')"%(fee,student_id,batch_id)
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")

	batch_id=request.POST.get('batchid7')
	timeslot_id=request.POST.get('timeslotid7')
	if batch_id and timeslot_id:
		query="insert into batch_timeslot(batch_id,timeslot_id) values('%d','%d')"%(int(batch_id),int(timeslot_id))
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully inserted")
		except:
			messages.error(request,"Insert correct values")


	query="SELECT * FROM student"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['student']=ans

	query="SELECT * FROM teacher"
	cur.execute(query)
	ans=cur.fetchall()
	ans=list(ans)
	for i in range(len(ans)):
		ans[i]=list(ans[i])
		ans[i].append(str(ans[i][4]))
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
	
	query="select student_id,batch.batch_id,student.name,teacher.name,subject,batch.standard,fee from (student natural join joins),(batch natural join teacher) where joins.batch_id=batch.batch_id order by student_id"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['joins']=ans

	query="select batch.batch_id,time_slot.timeslot_id,standard,subject,day,start_time,end_time from batch natural join batch_timeslot natural join time_slot order by batch_id,timeslot_id"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['batch_timeslot']=ans

	query="select batch.batch_id,student.student_id,standard,subject,name,dateofclass,record from attendance natural join student natural join batch order by batch_id,student_id,dateofclass"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['attendance']=ans

	query="select receipt_id,batch.batch_id,student.student_id,name,batch.standard,subject,dateofdeposit,amount from fee,student,batch where fee.student_id=student.student_id and fee.batch_id=batch.batch_id order by batch_id,student_id,dateofdeposit"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['fee']=ans	

	query="select comment_id,batch.batch_id,standard,subject,name,statement,timedate from comment natural join batch order by batch_id,timedate"
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['comment']=ans	

	return render(request,'management/dashboard.html',contextdata)

def deletestudent(request,pk):
	db,cur=connect()
	query="DELETE FROM student WHERE student_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deleteteacher(request,pk):
	db,cur=connect()
	query="DELETE FROM teacher WHERE teacher_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deleteclassroom(request,pk):
	db,cur=connect()
	query="DELETE FROM classroom WHERE classroom_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletebatch(request,pk):
	db,cur=connect()
	query="DELETE FROM batch WHERE batch_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletejoins(request,pk,qk):
	db,cur=connect()
	query="DELETE FROM joins WHERE student_id=('%d') and batch_id=('%d')"%(int(pk),int(qk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletebatchtimeslot(request,pk,qk):
	db,cur=connect()
	query="DELETE FROM batch_timeslot WHERE batch_id=('%d') and timeslot_id=('%d')"%(int(pk),int(qk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deleteattendance(request,pk,qk,rk):
	db,cur=connect()
	query="DELETE FROM attendance WHERE batch_id=('%d') and student_id=('%d') and dateofclass=('%s')"%(int(pk),int(qk),str(rk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletefee(request,pk):
	db,cur=connect()
	query="DELETE FROM fee WHERE receipt_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def deletecomment(request,pk):
	db,cur=connect()
	query="DELETE FROM comment where comment_id=('%d')"%(int(pk))
	cur.execute(query)
	db.commit()
	return redirect("dashboard")

def mlogout(request):
	if request.session.has_key("admin"):
		del request.session["admin"]
	return redirect("mlogin")