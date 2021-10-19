from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.BookUserListView.as_view()),
    path("users/<int:pk>/", views.BookUserDetailView.as_view()),
    path("comment/", views.CommentCreateView.as_view()),
    path("posts/<int:pk>/", views.PostDetailView.as_view()),
    path("message/", views.AddMessageView.as_view()),
    path("chats/<int:pk>/", views.ChatDetailView.as_view()),
]
