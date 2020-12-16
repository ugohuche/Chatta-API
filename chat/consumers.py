import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Friend_Request, Contact, Friends
from .views import get_last_10_messages, get_user_contact, get_current_chat, base64_file, get_friend_requests

class ChatConsumer(WebsocketConsumer):


    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)


    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        if (data['message_type'] == 'text') :
            message = Message.objects.create(
                contact=user_contact,
                content=data['message']
            )
        else :
            file_str = data['attachment']
            message = Message.objects.create(
                contact = user_contact,
                message_type = data['message_type'],
                content = data['message'],
                attachment = base64_file(file_str)
            )
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def message_to_json(self, message):
        if 'text' in message.message_type :
            return {
                'id': message.id,
                'author': message.contact.user.username,
                'pictureUrl': message.contact.profilePicture.url,
                'content': message.content,
                'attachment': '',
                'type': message.message_type,
                'timestamp': str(message.timestamp)
            }
        else :
            return {
                'id': message.id,
                'author': message.contact.user.username,
                'pictureUrl': message.contact.profilePicture.url,
                'content': message.content,
                'attachment': message.attachment.url,
                'type': message.message_type,
                'timestamp': str(message.timestamp)
            }


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data, bytes_data=None):
        message_data = json.loads(text_data)
        self.commands[message_data['command']](self, message_data)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))
 

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))






class Friend_RequestConsumer(WebsocketConsumer):

    def fetch_friends(self, data):
        contact = get_object_or_404(Contact, fullname=data['fullname'])
        contact_friends = get_object_or_404(Friends, contact=contact)
        friends = []
        for contact in contact_friends.friends:
            friends.append(self.friendContact_to_json(contact))
        content = {
            'command': 'friends',
            'friends': friends
        }
        self.send_request(content)


    def new_request(self, data):
        requester_contact = get_email_contact(data['from_user'])
        reciever_contact = get_email_contact(data['to_user'])
        message = data['message']
        friend_request = Friend_Request.objects.create(
            from_user=requester_contact,
            to_user=reciever_contact,
            message=message
        )
        friend_request.save()
        content = {
            'command': 'new_request',
            'request': self.request_to_json(friend_request)
        }
        return self.send_new_request(content)


    def fetch_requests(self, data):
        requests = get_friend_requests(data['email'])
        content = {
            'command': 'requests',
            'requests': self.requests_to_json(requests)
        }
        self.send_request(content)

    

    def deny_request(self, data):
        requestId = data['requestId']
        Friend_Request.objects.delete(id=requestId)
        


    def accept_request(self, data):
        Friend_Request.objects.delete(id=data['requestId'])
        firstContact = get_object_or_404(Contact, fullname=data['firstFullname']
        )
        secondContact = get_object_or_404(Contact, fullname=data['secondFullname'])
        firstFriend = get_object_or_404(Friends, contact=firstContact)
        firstFriend.friends.add(secondContact)
        firstFriend.save()
        secondFriend = get_object_or_404(Friends, contact=secondContact)
        secondFriend.friends.add(firstContact)
        secondFriend.save()
        friends = []
        friends.append(self.friendContact_to_json(firstContact))
        friends.append(self.friendContact_to_json(secondContact))
        content = {
            'command': 'update_friends',
            'friends': friends
        }
        return self.send_new_request(content)


    def friendContact_to_json(self, friendContact):
        return {
            'id': friendContact.id,
            'fullname': friendContact.fullname,
            'picture': friendContact.profilePicture
        }



    def requests_to_json(self, requests):
        results = []
        for request in requests:
            results.append(self.request_to_json(request))
        return results


        
    def request_to_json(self, request):
        return {
            'request_id': request.id,
            'from_user': request.from_user.fullname,
            'from_user_pic': request.from_user.profilePicture,
            'to_user': request.to_user.fullname,
            'to_user_email': request.to_user.user.email
        }

    
    def send_new_request(self, request):
        # Send request to room group
        async_to_sync(self.channel_layer.group_send)(
            self.user_group_name,
            {
                'type': 'friend_request',
                'request': request,
            }
        )


    def send_request(self, request):
        # Send requests to websocket
        self.send(text_data=json.dumps(request))

    
    # Recieve request from room group
    def friend_request(self, event):
        request = event['request']
        # Send request to websocket
        self.send(text_data=json.dumps(request))



    commands = {
        'fetch_friends': fetch_friends,
        'fetch_requests': fetch_requests,
        'new_request': new_request,
        'deny_request': deny_request,
        'accept_request': accept_request
    }


    def connect(self):
        self.user_email = self.scope['url_route']['kwargs']['user_email']
        self.user_group_name = 'requests_%s' % self.user_email

        # Join user group
        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave user group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name,
            self.channel_name
        )

    # Receive request from WebSocket
    def receive(self, text_data):
        request_data = json.loads(text_data)
        self.commands[request_data.command](self, request_data)