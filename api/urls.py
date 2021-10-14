from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.BookUserListView.as_view()),
    path("users/<int:pk>/", views.BookUserDetailView.as_view()),
]
