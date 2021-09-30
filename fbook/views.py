from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from django.contrib import messages

from .models import BookUser, Post, Invite
from .forms import RegisterUserForm, PostForm
from .mixins import PageMixin


class FLoginView(LoginView):
    template_name = 'fbook/login.html'


def index(request):
    if request.user.is_authenticated:
        return redirect('fbook:profile')
    return render(request, 'fbook/index.html')


@login_required
def profile(request):
    user = BookUser.objects.get(pk=request.user.id)
    posts = user.posts.all()
    context = {'user': user, 'posts': posts}
    return render(request, 'fbook/profile.html', context)


class RegisterUserView(CreateView):
    model = BookUser
    template_name = 'fbook/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('fbook:index')
    success_message = 'Пользователь успешно создан!'


class CreatePost(SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'fbook/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('fbook:profile')
    success_message = 'Пост добавлен!'

    def get_initial(self):
        user = self.request.user
        return {'user': user}


def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Пост удален!')
        return redirect('fbook:profile')
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


class UsersList(PageMixin, ListView):
    template_name = 'fbook/list_users.html'
    model = BookUser
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        q = Q(email='admin@admin.ru') | Q(pk=self.request.user.pk)
        objects = BookUser.objects.exclude(q)
        return objects





class UserDetail(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = BookUser
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        from_user = BookUser.objects.get(pk=self.request.user.pk)
        to_user = BookUser.objects.get(pk=context['user'].pk)
        exist_in_friends = from_user.friend.filter(email=to_user.email).exists()
        if exist_in_friends:
            context['already_friend'] = 'true'
        else:
            exist_in_offer = to_user.from_user.filter(to_user=from_user).exists()
            if exist_in_offer:
                context['exist_in_offer'] = 'true'
            else:
                exist = Invite.objects.filter(from_user=from_user, to_user=to_user).exists()
                if exist:
                    context['add_class'] = 'disabled'
                else:
                    context['add_class'] = ''
        return context


@login_required
def make_invite(request, pk):
    from_user = BookUser.objects.get(pk=request.user.pk)
    to_user = BookUser.objects.get(pk=pk)
    invite = Invite.objects.create(from_user=from_user, to_user=to_user)
    invite.save()
    return redirect('fbook:user_detail', pk=pk)


class OfferFriend(PageMixin,ListView):
    template_name = 'fbook/offer_friend.html'
    model = BookUser
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        current_user = BookUser.objects.get(pk=self.request.user.pk)
        return [user.from_user for user in current_user.to_user.all()]



