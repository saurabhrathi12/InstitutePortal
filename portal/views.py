from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import MySQLdb
import datetime

def start_student_session(request, user_id):
	request.session["user_mail_id"] = user_id
	request.session["student"] = user_id
	return request

def start_teacher_session(request, user_id):
	request.session["user_mail_id"] = user_id
	request.session["teacher"] = user_id
	return request

def check_if_auth_student(request):
	if request.session.has_key("user_mail_id") and request.session.has_key("student"):
		return request.session["user_mail_id"]
	else:
		return None

def check_if_auth_teacher(request):
	if request.session.has_key("user_mail_id") and request.session.has_key("teacher"):
		return request.session["user_mail_id"]
	else:
		return None

def stop_user_session(request):
	if request.session.has_key("user_mail_id"):
		del request.session["user_mail_id"]
		if request.session.has_key("student"):
			del request.session["student"]
		if request.session.has_key("teacher"):
			del request.session["teacher"]
		return True
	return False

def login(request):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	if check_if_auth_student(request):
		return redirect("student_dashboard")
	if check_if_auth_teacher(request):
		return redirect("teacher_dashboard")
	student_id=request.POST.get('student_id')
	dateofbirth=request.POST.get('dateofbirth')
	teacher_id=request.POST.get('teacher_id')
	password=request.POST.get('password')
	if student_id and dateofbirth:
		query="SELECT student_id, dateofbirth FROM student"
		cur.execute(query)
		ans=cur.fetchall()
		print ans
		for person in ans:
			if str(person[0])==student_id:
				if person[1]==str(dateofbirth):
					start_student_session(request,student_id)
					messages.success(request,"Sucessful Login")
					return redirect("student_dashboard")
				else:
					return render(request, 'portal/login.html')
		else:
			return render(request, 'portal/login.html')

	if teacher_id and password:
		query="SELECT teacher_id, password FROM teacher"
		cur.execute(query)
		ans=cur.fetchall()
		for person in ans:
			if str(person[0])==teacher_id:
				if person[1]==str(password):
					start_teacher_session(request,teacher_id)
					return redirect("teacher_dashboard")
				else:
					return render(request, 'portal/login.html')
		else:
			return render(request, 'portal/login.html')
	return render(request, 'portal/login.html')

def logout(request):
	stop_user_session(request)
	return redirect("login")

def student_dashboard(request):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_student(request)
	if not check:
		return redirect("login")
	check=int(check)
	query="SELECT * FROM student WHERE student_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()[0]
	contextdata={}
	contextdata['student']=ans
	
	query="SELECT batch_id,standard,subject,fee,name,mobile,address,hall_name,student_id FROM batch natural join joins natural join teacher natural join classroom WHERE student_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()
	ans=list(ans)
	for i in range(len(ans)):
		ans[i]=list(ans[i])
		query="SELECT day,start_time,end_time FROM batch natural join batch_timeslot natural join time_slot where batch_id=('%d')"%(ans[i][0])
		cur.execute(query)
		ans[i][8]=cur.fetchall()
	contextdata['batch']=ans
	return render(request, 'portal/studentdashboard.html', contextdata)

def student_attendance(request,pk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_student(request)
	if not check:
		return redirect("login")
	check=int(check)
	pk=int(pk)

	contextdata={}
	contextdata['student_id']=check
	query="SELECT name FROM student where student_id=('%d') " %(check)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['name']=ans[0][0]
	query="SELECT standard,subject FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	query="SELECT dateofclass,record FROM attendance WHERE student_id = ('%d') and batch_id = ('%d')"%(check,pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['attendance']=ans
	return render(request, 'portal/studentattendance.html',contextdata)

def student_fee(request,pk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_student(request)
	if not check:
		return redirect("login")
	check=int(check)
	pk=int(pk)

	contextdata={}
	contextdata['student_id']=check
	query="SELECT name FROM student where student_id=('%d') " %(check)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['name']=ans[0][0]
	query="SELECT standard,subject,fee FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	contextdata['totalfee']=ans[0][2]
	
	query="SELECT dateofdeposit,amount FROM fee WHERE student_id = ('%d') and batch_id = ('%d')"%(check,pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['fee']=ans
	feepaid=0
	for i in ans:
		feepaid=feepaid+i[1]
	contextdata['feepaid']=feepaid
	return render(request, 'portal/studentfee.html',contextdata)

def teacher_dashboard(request):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_teacher(request)
	if not check:
		return redirect("login")
	check=int(check)
	query="SELECT * FROM teacher WHERE teacher_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()[0]
	contextdata={}
	contextdata['teacher']=ans

	query="select batch_id,standard,subject,hall_name from batch natural join classroom where teacher_id= ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()
	ans=list(ans)
	for i in range(len(ans)):
		ans[i]=list(ans[i])
		query="SELECT day,start_time,end_time FROM batch natural join batch_timeslot natural join time_slot where batch_id=('%d')"%(ans[i][0])
		cur.execute(query)
		ans[i].append(cur.fetchall())
		query="SELECT count(student_id) FROM joins WHERE batch_id=('%d')"%(ans[i][0])
		cur.execute(query)
		ans[i].append(cur.fetchall()[0][0])
	contextdata['batch']=ans

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
		cur.execute(query)
		db.commit()
		#messages.success(request, "Successfully added")

	return render(request, 'portal/teacherdashboard.html',contextdata)

def teacher_attendance(request,pk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_teacher(request)
	if not check:
		return redirect("login")
	check=int(check)
	pk=int(pk)

	query="SELECT * FROM teacher WHERE teacher_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()[0]
	contextdata={}
	contextdata['teacher']=ans
	contextdata['id']=check

	query="SELECT standard,subject FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	query="SELECT student_id,name FROM student natural join joins WHERE batch_id = ('%d')"%(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['attendance']=ans

	date=request.POST.get('date')
	if date:
		date=datetime.datetime.strptime(date, '%Y-%m-%d').date()
		for i in range(1,len(ans)+1):
			name=request.POST.get(str(i))
			if name:
				print name
				if name=="Present":
					query="insert into attendance(student_id, batch_id, dateofclass, record) values ('%d','%d','%s','P')"%(ans[i-1][0],pk,date)
				else:
					query="insert into attendance(student_id, batch_id, dateofclass, record) values ('%d','%d','%s','A')"%(ans[i-1][0],pk,date)		
				cur.execute(query)
				db.commit()
	return render(request, 'portal/teacherattendance.html',contextdata)

def teacher_fee(request,pk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check = check_if_auth_teacher(request)
	if not check:
		return redirect("login")
	check=int(check)
	pk=int(pk)

	payid=request.POST.get('payid')
	amount=request.POST.get('amount')
	enrollid=request.POST.get('enrollid')
	enrollamount=request.POST.get('enrollamount')
	removeid=request.POST.get('removeid')

	if payid and amount:
		query="INSERT into fee(amount,dateofdeposit,student_id,batch_id) values('%d',curdate(),'%d','%d')"%(int(amount),int(payid),pk)
		cur.execute(query)
		db.commit()
	if enrollid:
		query="INSERT into joins(student_id,batch_id) values ('%d','%d')"%(int(enrollid),check)
		cur.execute(query)
		db.commit()
		query="INSERT into fee(amount,dateofdeposit,student_id,batch_id) values('%d',curdate(),'%d','%d')"%(int(enrollamount),int(enrollid),pk)
		cur.execute(query)
		db.commit()
	if removeid:
		query="DELETE from joins where student_id=('%s')"%(int(removeid))
		cur.execute(query)
		db.commit()
		query="DELETE from fee where student_id=('%s') and batch_id=('%d')"%(int(removeid),pk)
		cur.execute(query)
		db.commit()

	query="SELECT * FROM teacher WHERE teacher_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()[0]
	contextdata={}
	contextdata['id']=check
	contextdata['teacher']=ans
	query="SELECT standard,subject,fee FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	contextdata['totalfee']=ans[0][2]

	query="SELECT student_id,name,sum(amount) FROM student natural join fee where batch_id=('%d') group by student_id"%(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['fee']=ans

	return render(request, 'portal/teacherfee.html',contextdata)

def discussion(request,pk):
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	cur=db.cursor()
	check1 = check_if_auth_student(request)
	check2 = check_if_auth_teacher(request)
	if not check1 and not check2:
		return redirect("login")
	contextdata={}
	if check2:
		check=int(check2)
		query="SELECT name FROM teacher WHERE teacher_id = ('%d')"%(check)
		cur.execute(query)
		ans=cur.fetchall()
		contextdata['name']=ans[0][0]
	if check1:
		check=int(check1)
		query="SELECT name FROM student WHERE student_id = ('%d')"%(check)
		cur.execute(query)
		ans=cur.fetchall()
		contextdata['name']=ans[0][0]
	pk=int(pk)

	statement=request.POST.get('statement')
	if statement:
		query="insert into comment(page_id, statement, name, timedate) values('%d','%s', '%s' , now());"%(pk,statement,contextdata['name'])
		cur.execute(query)
		db.commit()
	query="SELECT standard,subject FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	query="SELECT * FROM comment where page_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['comment']=ans
	return render(request, 'portal/discussion.html',contextdata)
