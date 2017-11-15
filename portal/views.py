from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib import messages
import MySQLdb
import datetime
import hashlib
from uuid import uuid4
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext

def connect():
	db=MySQLdb.connect(host="localhost",user="root",passwd="qwerty123",db="institute")
	#db=MySQLdb.connect(host="rathiclasses.mysql.pythonanywhere-services.com",user="rathiclasses",passwd="qwerty123",db="rathiclasses$institute")
	cur=db.cursor()
	return db,cur

def start_student_session(request, user_id,dateofbirth):
	request.session["user_mail_id"] = user_id
	request.session["student"] = user_id
	request.session["dateofbirth"]=dateofbirth
	return request

def start_teacher_session(request, user_id,password):
	request.session["user_mail_id"] = user_id
	request.session["teacher"] = user_id
	request.session["password"]= password
	return request

def check_if_auth_student(request):
	if request.session.has_key("user_mail_id") and request.session.has_key("student") and request.session.has_key("dateofbirth"):
		db,cur=connect()
		query="SELECT dateofbirth FROM student WHERE student_id = ('%d')"%(int(request.session["student"]))
		cur.execute(query)
		try:
			ans=cur.fetchall()[0]
		except:
			return None
		if str(ans[0])==request.session["dateofbirth"]:
			return request.session["user_mail_id"]
	return None

def check_if_auth_teacher(request):
	if request.session.has_key("user_mail_id") and request.session.has_key("teacher") and request.session.has_key("password"):
		db,cur=connect()
		query="SELECT password FROM teacher WHERE teacher_id = ('%d')"%(int(request.session["teacher"]))
		cur.execute(query)
		try:
			ans=cur.fetchall()[0]
		except:
			return None
		if str(ans[0])==request.session["password"]:
			return request.session["user_mail_id"]
	return None

def stop_user_session(request):
	if request.session.has_key("user_mail_id"):
		del request.session["user_mail_id"]
		if request.session.has_key("student"):
			del request.session["student"]
			if request.session.has_key("dateofbirth"):
				del request.session["dateofbirth"]
		if request.session.has_key("teacher"):
			del request.session["teacher"]
			if request.session.has_key("password"):
				del request.session["password"]
		return True
	return False

def login(request):
	db,cur=connect()
	if check_if_auth_student(request):
		return redirect("student_dashboard")
	if check_if_auth_teacher(request):
		return redirect("teacher_dashboard")
	student_id=request.POST.get('student_id')
	dateofbirth=request.POST.get('dateofbirth')
	teacher_id=request.POST.get('teacher_id')
	password=request.POST.get('password')
	if student_id and dateofbirth:
		d=dateofbirth
		dateofbirth=d[4]+d[5]+d[6]+d[7]+'-'+d[2]+d[3]+'-'+d[0]+d[1]
		query="SELECT student_id, dateofbirth FROM student"
		cur.execute(query)
		ans=cur.fetchall()
		ans=list(ans)
		for i in range(len(ans)):
			ans[i]=list(ans[i])
			ans[i][1]=str(ans[i][1])
		for person in ans:
			if str(person[0])==student_id:
				if person[1]==dateofbirth:
					start_student_session(request,student_id,dateofbirth)
					messages.success(request,"Sucessful Login")
					return redirect("student_dashboard")
		messages.error(request,"Wrong username and/or password")
		return render(request, 'portal/login.html')

	if teacher_id and password:
		password=hashlib.sha512(password).hexdigest()
		query="SELECT teacher_id, password FROM teacher"
		cur.execute(query)
		ans=cur.fetchall()
		for person in ans:
			if str(person[0])==teacher_id:
				if person[1]==password:
					start_teacher_session(request,teacher_id,password)
					messages.success(request,"Sucessful Login")
					return redirect("teacher_dashboard")
		messages.error(request,"Wrong username and/or password")
		return render(request, 'portal/login.html')	
	return render(request, 'portal/login.html')

def logout(request):
	stop_user_session(request)
	#messages.success(request,"Logged out successfully")
	return redirect("login")

def student_dashboard(request):
	db,cur=connect()
	check = check_if_auth_student(request)
	if not check:
		return redirect("login")
	check=int(check)
	query="SELECT * FROM student WHERE student_id = ('%d')"%(check)
	cur.execute(query)
	try:
		ans=cur.fetchall()[0]
	except:
		return redirect("logout")
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
	db,cur=connect()
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

@csrf_protect
@csrf_exempt
def student_fee(request,pk):
	db,cur=connect()
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

	MERCHANT_KEY = "iRheZLj2"
	key="iRheZLj2"
	SALT = "KJfs9LzBqo"
	PAYU_BASE_URL = "https://secure.payu.in/_payment"
	action = ''
	posted={}
	for i in request.POST:
		posted[i]=request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid']=txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key']=key
	posted['firstname']=check
	posted['productinfo']=pk
	posted['surl']="https://rathiclasses.pythonanywhere.com/success"
	posted['furl']="https://rathiclasses.pythonanywhere.com/failure"
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''
		hash_string+='|'
	hash_string+=SALT
	hashh=hashlib.sha512(hash_string).hexdigest().lower()
	action =PAYU_BASE_URL
	if posted.get("email")!=None and posted.get("amount")!=None and posted.get("phone")!=None:
		return render_to_response('portal/current_datetime.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://secure.payu.in/_payment" })
	return render(request, 'portal/studentfee.html',contextdata)

@csrf_protect
@csrf_exempt
def success(request):
	c = {}
	c.update(csrf(request))
	try:
		status=request.POST["status"]
	except:
		return redirect(login)
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="KJfs9LzBqo"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a payment of Rs. ", amount ,". Your order will soon be shipped."
	db,cur=connect()
	query="INSERT into fee(amount,dateofdeposit,student_id,batch_id) values('%d',curdate(),'%d','%d')"%(int(float(amount)),int(firstname),int(productinfo))
	cur.execute(query)
	db.commit()
	return render_to_response('portal/success.html',RequestContext(request,{"txnid":txnid,"status":status,"amount":amount}))


@csrf_protect
@csrf_exempt
def failure(request):
	c = {}
	c.update(csrf(request))
	try:
		status=request.POST["status"]
	except:
		return redirect(login)
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="KJfs9LzBqo"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a fee payment of Rs. ", amount
	return render_to_response("portal/failure.html",RequestContext(request,c))


def teacher_dashboard(request):
	db,cur=connect()
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
	password=request.POST.get('password')
	
	if name and standard and school and father_name and mother_name and mobile and address and dateofbirth:
		standard=int(standard)
		dateofbirth=datetime.datetime.strptime(dateofbirth, '%Y-%m-%d').date()
		query="insert into student(name,mobile,dateofbirth,address,father_name,mother_name,standard,school) values('%s','%s','%s','%s','%s','%s','%d','%s')"%(name,mobile,dateofbirth,address,father_name,mother_name,standard,school)
		try:
			cur.execute(query)
			db.commit()
			messages.success(request, "Successfully added")
		except:
			messages.error(request, "Enter correct values")

	if password:
		password=hashlib.sha512(password).hexdigest()
		query="update teacher set password='%s' where teacher_id='%d' "%(password,check)
		cur.execute(query)
		db.commit()
		del request.session["password"]
		request.session["password"]=password
	return render(request, 'portal/teacherdashboard.html',contextdata)

def teacher_attendance(request,pk):
	db,cur=connect()
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
	contextdata['batch_id']=pk

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
		try:
			for i in range(1,len(ans)+1):
				name=request.POST.get(str(i))
				if name:
					if name=="Present":
						query="insert into attendance(student_id, batch_id, dateofclass, record) values ('%d','%d','%s','P')"%(ans[i-1][0],pk,date)
					else:
						query="insert into attendance(student_id, batch_id, dateofclass, record) values ('%d','%d','%s','A')"%(ans[i-1][0],pk,date)						
					cur.execute(query)
			db.commit()
		except:
			messages.error(request,"Values already entered for the date")
	return render(request, 'portal/teacherattendance.html',contextdata)

def teacher_fee(request,pk):
	db,cur=connect()
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
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfull payment done")
		except:
			messages.error(request,"Enter correct values")
	if enrollid and enrollamount:
		try:
			query="INSERT into joins(student_id,batch_id) values ('%d','%d')"%(int(enrollid),pk)
			cur.execute(query)
			query="INSERT into fee(amount,dateofdeposit,student_id,batch_id) values('%d',curdate(),'%d','%d')"%(int(enrollamount),int(enrollid),pk)
			cur.execute(query)
			db.commit()
		except:
			messages.error(request,"Enter correct values")
	if removeid:
		query="DELETE from joins where student_id=('%d') and batch_id=('%d')"%(int(removeid),pk)
		cur.execute(query)
		db.commit()

	query="SELECT * FROM teacher WHERE teacher_id = ('%d')"%(check)
	cur.execute(query)
	ans=cur.fetchall()[0]
	contextdata={}
	contextdata['id']=check
	contextdata['teacher']=ans
	contextdata['batch_id']=pk
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
	db,cur=connect()
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
		query="insert into comment(batch_id, statement, name, timedate) values('%d','%s', '%s' , now());"%(pk,statement,contextdata['name'])
		try:
			cur.execute(query)
			db.commit()
			messages.success(request,"Successfully posted")
		except:
			messages.error(request,"Insert correct values")
	query="SELECT standard,subject FROM batch where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['standard']=ans[0][0]
	contextdata['subject']=ans[0][1]
	query="SELECT * FROM comment where batch_id=('%d') " %(pk)
	cur.execute(query)
	ans=cur.fetchall()
	contextdata['comment']=ans
	return render(request, 'portal/discussion.html',contextdata)