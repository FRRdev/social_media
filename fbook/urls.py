from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'fbook'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.FLoginView.as_view(), name='login'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('post/create/', views.CreatePost.as_view(), name='post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('users/', views.UsersList.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/invite/<int:pk>', views.make_invite, name='invite'),
]
