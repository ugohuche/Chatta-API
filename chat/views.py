from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Chat, Contact, Friend_Request
from django.core.files.base import ContentFile
import base64

def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def get_friend_requests(email):
    contact = get_email_contact(email)
    query_set = Friend_Request.objects.filter(Q(from_user=contact) | Q(to_user=contact))
    return query_set.order_by('-timestamp').all()

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)

def get_email_contact(email):
    user = get_object_or_404(User, email=email)
    return get_object_or_404(Contact, user=user)

def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
    
def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(':')[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))