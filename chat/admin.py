from django.contrib import admin

from .models import Message, Chat, Contact, Friends

admin.site.register(Contact)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Friends)
