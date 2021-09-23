from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import BookUser
from .forms import RegisterUserForm


class FLoginView(LoginView):
    template_name = 'fbook/login.html'



def index(request):
    if request.user.is_authenticated:
        return redirect('fbook:profile')
    return render(request, 'fbook/index.html')


@login_required
def profile(request):
    user = BookUser.objects.get(pk=request.user.id)
    context = {'user': user}
    return render(request, 'fbook/profile.html', context)


class RegisterUserView(CreateView):
    model = BookUser
    template_name = 'fbook/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('fbook:index')
    success_message = 'Пользователь успешно создан!'
