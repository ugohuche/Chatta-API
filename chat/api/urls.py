from django.urls import path, re_path

from .views import (
	ChatDeleteView,
	ChatCreateView,
	ChatDetailView,
	ChatUpdateView,
	ChatListView,
	MessageDetailView,
	MessageListView,
	ContactUpdateAPIView,
	ContactDetailByIdView,
	ContactDetailBySlugView,
	ContactDetailByFullnameView,
	FriendsDetailView,
	PasswordChangeView
)

urlpatterns = [
	path('api/change-password', PasswordChangeView.as_view()),
	path('create', ChatCreateView.as_view()),
	path('<pk>', ChatDetailView.as_view()),
	path('<pk>/update', ChatUpdateView.as_view()),
	path('<pk>/delete', ChatDeleteView.as_view()),
	path('', ChatListView.as_view()),
	path('message/<pk>', MessageDetailView.as_view()),
	path('message', MessageListView.as_view()),
	path('contact/profile/<slug>', ContactDetailBySlugView.as_view()),
	path('contact/profileById/<pk>', ContactDetailByIdView.as_view()),
	path('contact/profileByName/<fullname>', ContactDetailByFullnameView.as_view()),
	path('contact/profile/<slug>/update', ContactUpdateAPIView.as_view()),
	path('contact/friends/<slug>', FriendsDetailView.as_view())
]