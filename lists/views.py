from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.http import HttpResponse
from rest_framework import filters,generics
import json
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Notification as NotificationModel
class UserList(APIView):

	def get(self,request):
		lists=User.objects.all()
		serializer=UserSerializer(lists,many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer=UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=201)
		return HttpResponse(serializer.errors,status=204)


class UserListDetail(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	#TOKEN FOR ADMIN : token 3cec7dc3ad20a8f2b39bddd9936b6131555dc112
	def get(self,request,pk):
		if pk:
			user_object=get_object_or_404(User,id=pk)
			serializer=UserSerializer(user_object,context={'request':request})
			todo=Todo.objects.all()
			return Response(serializer.data,status=200)
		else:
			return HttpResponse('empty',status=404)

	def delete(self,request,pk):
		snippet=get_object_or_404(User,id=pk)
		snippet.delete()
		return Response(status=204)



class NotificationView(APIView):

	def get(self,request,pk=None):
		queryset=NotificationModel.objects.all()
		if pk:
			queryset=queryset.filter(id=pk)
		serializer=NotificationSerializer(queryset,many=True,context={'request':request})
		return Response(serializer.data,status=200)

	def post(self,request):
		serializer=NotificationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=201)
		return Response(serializer.errors,status=204)




class TodoList(APIView):

	def get(self,request,pk=None):
		queryset=Todo.objects.all()
		username=self.request.query_params.get('f_name',None)
		if pk:
			queryset=queryset.filter(id=pk)
		serializer=TodoSerializer(queryset,many=True,context={'request':request})
		if username:
			queryset = queryset.filter(users__f_name=username)
			serializer=TodoSerializer(queryset,many=True,context={'request':request})
		return Response(serializer.data,status=200)


	def post(self,request):
		serializer=TodoSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=201)
		return Response(serializer.errors,status=400)

	def delete(self,request,pk,format=None):
		snippet=get_object_or_404(Todo,id=pk)
		snippet.delete()
		return Response(status=204)

	def patch(self,request,pk):
		todo_object=get_object_or_404(Todo,id=pk)
		request_data=request.data
		change=request_data.get("status",None)

		attachment = request_data.get("attachment",None)
		if attachment:
				for x in request_data["attachment"]:
					todo_object.attachment.add(x)
					serializer=IssueSerializer(todo_object)
				return Response(serializer.data,status=200)

		serializer=TodoSerializer(data=request_data, instance=todo_object, partial=True)
		if serializer.is_valid():
			if(todo_object.status==1 and change==2):
				serializer.save()
				return Response(serializer.data,status=200)
			elif(todo_object.status==2 and change==1):
				serializer.save()
				return Response(serializer.data,status=200)
			elif(todo_object.status==2 and change==3):
				serializer.save()
				return Response(serializer.data,status=200)
			#State 3 can change to any state
			elif(todo_object.status==3):
				serializer.save()
				return Response(serializer.data,status=200)
			else:
				return Response("NOT ALLOWED !",status=400)




class FileUploadView(APIView):

	def get(self,request,pk=None):
		queryset=Attachment.objects.all()
		if pk:
			queryset=queryset.filter(id=pk)
		serializer=AttachmentSerializer(queryset,many=True,context={'request':request})
		return Response(serializer.data,status=200)

	def post(self,request,format=None):
		file_object=request.data['document']
		serializer=AttachmentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=201)
		return Response(serializer.data,status=204)


#Implemented this to see how it works. Had used query_params.get("order",None) earlier. Then sorted using order_by()
class Order(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']

