from django.shortcuts import get_object_or_404
from django.db.models import Q 
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
	GenericAPIView,
	ListAPIView,
	RetrieveAPIView,
	DestroyAPIView,
	UpdateAPIView,
	CreateAPIView,
	ListCreateAPIView,
	RetrieveUpdateAPIView
)
from chat.models import Chat, Contact, Message, Friends, Friend_Request
from chat.views import get_user_contact
from .serializers import (
	ChatSerializer,
	MessageSerializer,
	MessageListSerializer, 
	ContactSlugSerializer, 
	FriendsSerializer,
	ContactIdSerializer,
	PasswordChangeSerializer,
	Friend_RequestSerializer
)


class PasswordChangeView(UpdateAPIView):
	"""
	Endpoint for changing password
	"""
	serializer_class = PasswordChangeSerializer
	model = User
	permission_class = (permissions.IsAuthenticated)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj
	
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ['Wrong Password.']}, status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			response = {
				'status': 'success',
				'code': status.HTTP_200_OK,
				'message': 'Password successfully updated',
				'data': []
			}

			return Response(response)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChatListView(ListAPIView):
	serializer_class = ChatSerializer
	permission_class = (permissions.IsAuthenticated, )

	def get_queryset(self):
		queryset = Chat.objects.all()
		username = self.request.query_params.get('username', None)
		if username != None:
			contact = get_user_contact(username)
			queryset = contact.chats.all()
		return queryset



class ChatDetailView(RetrieveAPIView):
	queryset = Chat.objects.all()
	serializer_class = ChatSerializer
	permission_class = (permissions.IsAuthenticated, )


class ChatCreateView(ListCreateAPIView):
	queryset = Chat.objects.all()
	serializer_class = ChatSerializer
	permission_class = (permissions.IsAuthenticated, )

	def perform_create(self, serializer):
		if serializer.is_valid(raise_exception=True):
			return serializer.save()


class ChatUpdateView(UpdateAPIView):
	queryset = Chat.objects.all()
	serializer_class = ChatSerializer
	permission_class = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
	queryset = Chat.objects.all()
	serializer_class = ChatSerializer
	permission_class = (permissions.IsAuthenticated, )


class MessageDetailView(RetrieveAPIView):
	serializer_class = MessageSerializer
	permission_class = (permissions.IsAuthenticated, )
	queryset = Message.objects.all()


class MessageListView(ListAPIView):
	serializer_class = MessageListSerializer
	permission_class = (permissions.AllowAny, )

	def get_queryset(self):
		username = self.request.query_params.get('username', None)
		contact = get_user_contact(username)
		# queryset = contact.messages.get_attachments()[:4]
		queryset = contact.messages.all()
		filtered = queryset.filter(Q(message_type='image/jpeg') | Q(message_type='video/mp4'))
		return filtered[:4]


	

class ContactUpdateAPIView(UpdateAPIView):
	queryset = Contact.objects.all()
	serializer_class = ContactSlugSerializer
	permission_class = (permissions.IsAuthenticated, )
	lookup_field = 'slug'

class ContactDetailBySlugView(RetrieveAPIView):
	serializer_class = ContactSlugSerializer
	permission_class = (permissions.IsAuthenticated, )
	queryset = Contact.objects.all()
	lookup_field = 'slug'

class ContactDetailByIdView(RetrieveAPIView):
	serializer_class = ContactIdSerializer
	permission_class = (permissions.IsAuthenticated, )
	queryset = Contact.objects.all()
	lookup_field = 'pk'

class ContactDetailByFullnameView(RetrieveAPIView):
	serializer_class = ContactSlugSerializer
	permission_class = (permissions.IsAuthenticated, )
	queryset = Contact.objects.all()
	lookup_field = 'fullname'



class FriendsDetailView(RetrieveAPIView):
	serializer_class = FriendsSerializer
	permission_class = (permissions.IsAuthenticated, )
	queryset = Friends.objects.all()
	lookup_field = 'slug'


class Friend_RequestListView(ListAPIView):
	serializer_class = Friend_RequestSerializer
	permission_class = (permissions.IsAuthenticated, )

	def get_queryset(self):
		username = self.request.query_params.get('username', None)
		contact = get_user_contact(username)
		queryset = contact.requests_recieved.all()
		return queryset
