from .models import *
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
	id=serializers.IntegerField(read_only=True)
	f_name=serializers.CharField()
	l_name=serializers.CharField()
	new_notif=serializers.IntegerField(read_only=True)
	full_name=serializers.SerializerMethodField(read_only=True)
	def get_full_name(self,obj):
		return (obj.f_name+" "+obj.l_name)

	def create(self,validated_data):
		return User.objects.create(**validated_data)


class AttachmentSerializer(serializers.Serializer):
	id=serializers.IntegerField(read_only=True)
	document=serializers.FileField()

	def get_document_url(self,obj):
		return obj.document.url 

	def create(self,validated_data):
		return Attachments.objects.create(**validated_data)


class TodoSerializer(serializers.Serializer):
	id=serializers.IntegerField(read_only=True)
	title=serializers.CharField()
	desc=serializers.CharField()
	status=serializers.IntegerField()
	created=serializers.DateTimeField(read_only=True)
	updated=serializers.DateTimeField(read_only=True)
	users=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	attachment=serializers.PrimaryKeyRelatedField(queryset=Attachment.objects.all(),many=True,required=False)
	attachment_details=AttachmentSerializer(read_only=True,many=True,source='attachment')
	marked=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True,required=False)
	marked_details=UserSerializer(read_only=True,many=True)

	def create(self,validated_data):
		attach=validated_data.pop('attachment',None)
		todo = Todo.objects.create(**validated_data)
		if attach:
			todo.attachment.set(attach)
			todo.save()
		return todo

	def update(self, instance, validated_data):
		instance.id=validated_data.get('id',instance.id)
		instance.title=validated_data.get('title',instance.title)
		instance.desc=validated_data.get('desc',instance.desc)
		instance.status=validated_data.get('status',instance.status)
		instance.created=validated_data.get('created',instance.created)
		instance.updated=validated_data.get('updated',instance.updated)
		instance.users=validated_data.get('users',instance.users)
		# instance.marked=validated_data.get('validated_data',validated_data)
		attach=validated_data.pop('attachment',None)
		if attach:
			instance.attachment.set(attach)
		instance.save()
		return instance

class NotificationSerializer(serializers.Serializer):
	id=serializers.IntegerField(read_only=True)
	state=serializers.IntegerField()
	new_state=serializers.IntegerField()
	todo_user_id=serializers.IntegerField()
	todos=serializers.PrimaryKeyRelatedField(queryset=Todo.objects.all())
	
	change=serializers.SerializerMethodField(read_only=True)
	def get_change(self,obj):
		return (str(obj.state)+" in "+str(obj.todo_user_id)+" changed to "+str(obj.new_state))

	def create(self,validated_data):
		return Notification.objects.create(**validated_data)