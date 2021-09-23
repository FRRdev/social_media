from django.urls import path
from . import views

app_name = 'fbook'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.FLoginView.as_view(), name='login'),
    path('accounts/register/',views.RegisterUserView.as_view(),name='register'),
    path('profile/', views.profile, name='profile')
]
