from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ..views import get_email_contact
from chat.models import Chat, Message, Contact, Friends, Friend_Request

class PasswordChangeSerializer(serializers.Serializer):
	model = User

	"""
	Serializer for password change.
	"""
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	

class ParticipantSerializer(serializers.StringRelatedField):
	def to_internal_value(self, value):
		return value
		

class ChatSerializer(serializers.ModelSerializer):
	participants = ParticipantSerializer(many=True)
	admins = ParticipantSerializer(many=True)

	class Meta:
		model = Chat
		fields = ('__all__')

	def create(self, validated_data):
		participants = validated_data.pop('participants')
		admins = validated_data.pop('admins')
		chat = Chat()
		chat.save()
		for fullname in participants:
			contact = get_object_or_404(Contact, fullname=fullname)
			chat.participants.add(contact)
		for admin in admins:
			adminContact = get_object_or_404(Contact, fullname=admin)
			chat.admins.add(adminContact)
		if validated_data['chatType'] == 'GC':
			chatName =  validated_data.pop('chatName')
			chat.chatName = chatName
		chatType = validated_data.pop('chatType')
		chat.chatType = chatType
		chat.save()
		return chat

class MessageSerializer(serializers.ModelSerializer):

	class Meta:
		model = Message
		fields = ('id', 'content', 'timestamp', 'contact', 'message_type')


class MessageListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Message
		fields = ('attachment', 'message_type')



class ContactSlugSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = ('id', 'fullname', 'profilePicture', 'city', 'about', 'phoneNumber')



class ContactIdSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = ('fullname', 'profilePicture')




class FriendsSerializer(serializers.ModelSerializer):
	friends = ParticipantSerializer(many=True)

	class Meta:
		model = Friends
		fields = ('contact', 'friends')
	

class Friend_RequestSerializer(serializers.ModelSerializer):

	class Meta:
		model = Friend_Request
		fields = ('__all__')