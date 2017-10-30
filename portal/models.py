from __future__ import unicode_literals
from django.db import models
import datetime

"""
class Teacher(models.Model):
	username=models.CharField(max_length=50,primary_key=True)
	password=models.CharField(max_length=50)
	name=models.CharField(max_length=100)
	mobile=models.CharField(max_length=10)
	dateofbirth=models.DateField()
	address=models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Student(models.Model):
	student_id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=100)
	mobile=models.CharField(max_length=10)
	dateofbirth=models.CharField(max_length=8)
	address=models.CharField(max_length=200)
	father_name=models.CharField(max_length=100)
	mother_name=models.CharField(max_length=100)
	standard=models.IntegerField()
	school=models.CharField(max_length=100)
	def __str__(self):
		return str(self.student_id)+" "+self.name

class Batch(models.Model):
	batch_id=models.AutoField(primary_key=True)
	standard=models.IntegerField()
	subject=models.CharField(max_length=50)
	teacher=models.ForeignKey(Teacher)
	#page=models.ForeignKey(Discussion_page)
	#classroom=models.ForeignKey(Classroom)
	def __str__(self):
		return str(self.standard)+"th "+self.subject+" "+(self.teacher).name


class Discussion_page(models.Model):
	page_id=models.AutoField(primary_key=True)


class Comment(models.Model):
	comment_id=models.AutoField(primary_key=True)	
	statement=models.TextField()
	page_id=models.ForeignKey(Discussion_page)
	#author- student or teacher
	time=models.DateTimeField()

class TimeSlot(models.Model):
	timeslot_id=models.AutoField(primary_key=True)
	day=models.CharField(max_length=10)
	start_time=models.IntegerField()
	end_time=models.IntegerField()

class Classroom(models.Model):
	room_id=models.AutoField(primary_key=True)
	hall_name=models.CharField(max_length=50)
	capacity=models.IntegerField()

"""