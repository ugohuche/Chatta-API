from django.db import models
from django.db.models import Q 
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

CHAT_TYPE_CHOICES = (
	('DM', 'Direct Message'),
	('GC', 'Group Chat')
)  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
	email_message = f"Follow this link to reset your password http://localhost:1234/password_reset/confirm?token={reset_password_token.key}"

	send_mail(
		# title:
		"Password Reset for {title}".format(title="Chatta.com"),
		# message:
		email_message,
		# from:
		"ucugooh@outlook.com",
		# to:
		[reset_password_token.user.email]
	)


class Contact(models.Model):
	user = models.ForeignKey(User, related_name='contact', on_delete=models.CASCADE)
	profilePicture = models.ImageField()
	fullname = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=20, blank=True)
	about = models.TextField(blank=True)
	phoneNumber = models.CharField(max_length=20, blank=True)
	slug = models.SlugField()

	def __str__(self):
		return f"{self.fullname}/{self.user.username}/{self.pk}"


def user_directory_path(instance, filename):
	return f'message_file_{instance.contact.user.username}/{filename}'


class Friends(models.Model):
	contact = models.ForeignKey(Contact, related_name='contactFriends', on_delete=models.CASCADE)
	friends = models.ManyToManyField(Contact, blank=True)
	slug = models.SlugField()

	def __str__(self):
		return self.contact.fullname



class Friend_Request(models.Model):
	from_user = models.ForeignKey(Contact, related_name="requests_sent", on_delete=models.CASCADE)
	to_user = models.ForeignKey(Contact, related_name="requests_recieved", on_delete=models.CASCADE, verbose_name ="User to invite")
	message = models.CharField(max_length=300, blank=True, verbose_name="Optional message", help_text="It's always nice to add a friendly message")
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.from_user.fullname} to {self.to_user.fullname}'




class MessageQuerySet(models.QuerySet):
	def get_attachments(self):
		return self.filter(
			Q(message_type='image/jpeg') | Q(message_type='video/mp4')
		)


class Message(models.Model):
	contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
	message_type = models.CharField(default='text', max_length=20)
	content = models.TextField(blank=True, null=True)
	attachment = models.FileField(blank=True, null=True, upload_to=user_directory_path)
	is_read = models.BooleanField(default=False)
	is_sent = models.BooleanField(default=False)
	is_recieved = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = MessageQuerySet.as_manager()

	def __str__(self):
		return f"{self.contact.user.username}/{self.pk}"

class Chat(models.Model):
	participants = models.ManyToManyField(Contact, related_name='chats')
	admins = models.ManyToManyField(Contact, related_name='chatAdmins')
	messages = models.ManyToManyField(Message, blank=True)
	chatType = models.CharField(max_length=3, default='GC', choices=CHAT_TYPE_CHOICES)
	chatPicture = models.ImageField(blank=True, null=True)
	chatName = models.CharField(max_length=20, blank=True, null=True)

	def __str__(self):
		return "{}".format(self.pk)