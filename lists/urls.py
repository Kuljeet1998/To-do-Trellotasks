from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
urlpatterns=[
	path('users/',UserList.as_view()),
	path('users/<int:pk>/',UserListDetail.as_view()),
	path('todo/',TodoList.as_view()),
	path('todo/<int:pk>/',TodoList.as_view()),
	url('^todo/(?P<f_name>.+)/$',TodoList.as_view()),
	path('fileupload/',FileUploadView.as_view()),
	path('fileupload/<int:pk>/',FileUploadView.as_view()),
	path('todo/order/',Order.as_view()),
	path('notif/',NotificationView.as_view()),
	path('notif/<int:pk>/',NotificationView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)