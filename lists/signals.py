from django.contrib.auth.models import *
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import *
from rest_framework.response import Response

@receiver(pre_save,sender=Todo)
def on_change(sender,instance:Todo,**kwargs):
	prev=Todo.objects.get(id=instance.id)
	if prev.status != instance.status:
		Notification.objects.create(state=prev.status,new_state=instance.status,todo_user_id=instance.id,todos=prev)
		if prev.marked is not None:
			print(type(prev.marked))
			for x in prev.marked.all():
				print(x.id)
				user_obj=User.objects.get(id=x.id)
				user_obj.new_notif+=1
				user_obj.save()

#notif will be decreased if user has deleted the notification (which means he has seen the new notification)
# @receiver(post_delete,sender=Notification)
# def on_delete(sender,instance,**kwargs):