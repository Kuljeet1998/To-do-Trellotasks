from django.db import models
import datetime
from django.dispatch import receiver
# Create your models here.
class User(models.Model):
	first_name=models.CharField(max_length=15)
	last_name=models.CharField(max_length=15)
	new_notif=models.IntegerField(default=0)

	def __str__(self):
		return self.f_name+" w "+str(self.new_notif)+" notification(s)"


class Attachment(models.Model):
	document=models.FileField(upload_to='document/')
	def __str__(self):
		return str(self.id)


class Todo(models.Model):
	STATE=((1,'To be done'),(2,'In progress'),(3,'Done'))
	title=models.CharField(max_length=25)
	desc=models.TextField(max_length=100)
	status=models.IntegerField(default=1,choices=STATE)
	created=models.DateTimeField(auto_now=True)
	updated=models.DateTimeField(auto_now=True)
	users=models.ForeignKey(User,on_delete=models.CASCADE, related_name='todos')
	attachment=models.ManyToManyField(Attachment, related_name="todos") #DELAY
	marked=models.ManyToManyField(User,related_name="todos")
	
	def __str__(self):
		return self.title

class Notification(models.Model):
	state=models.IntegerField()
	new_state=models.IntegerField(default=0)
	todo_user_id=models.IntegerField(default=0)
	todos=models.ForeignKey(Todo,on_delete=models.CASCADE,related_name="notifications")

	def __str__(self):
		str1="State "+str(self.state)+" changed to "+str(self.new_state)+" in "+str(self.todo_user_id)
		return str1