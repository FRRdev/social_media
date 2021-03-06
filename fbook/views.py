from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from django.contrib import messages
import json

from .models import BookUser, Post, Invite, Chat, Message, Comment, Like
from .forms import RegisterUserForm, PostForm, SendMessageForm, SearchForm, UserCommentForm
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
    context = {'user': user}
    list_of_posts_with_like = []
    for post in user.posts.all():
        if Like.objects.filter(from_user=user, post=post).exists():
            list_of_posts_with_like.append(post.pk)
    context['list_likes'] = list_of_posts_with_like
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
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            q = Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
            objects = objects.filter(q)

        return objects

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
        else:
            keyword = ''
        form = SearchForm(initial={'keyword': keyword})
        data['form'] = form
        return data


class UserDetail(SuccessMessageMixin, LoginRequiredMixin, DetailView):
    model = BookUser
    context_object_name = 'user'

    def post(self, request, *args, **kwargs):
        id_user = self.get_object().pk
        if request.method == "POST":
            form = UserCommentForm(request.POST)
            post = Post.objects.get(pk=request.POST.get('post', None))
            if form.is_valid():
                content = form['content'].value()
                author = BookUser.objects.get(pk=form['author'].value())
                comment = Comment.objects.create(author=author, content=content, post=post)
                comment.save()
                return redirect('fbook:user_detail', pk=id_user)
            return redirect('fbook:user_detail', pk=id_user)

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        from_user = BookUser.objects.get(pk=self.request.user.pk)
        to_user = BookUser.objects.get(pk=context['user'].pk)
        initial = {
            'author': from_user.pk,
        }
        form = UserCommentForm(initial=initial)
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
        list_of_posts_with_like = []
        for post in to_user.posts.all():
            if Like.objects.filter(from_user=from_user, post=post).exists():
                list_of_posts_with_like.append(post.pk)
        context['list_likes'] = list_of_posts_with_like
        context['form'] = form
        return context


@login_required
def make_invite(request, pk):
    from_user = BookUser.objects.get(pk=request.user.pk)
    to_user = BookUser.objects.get(pk=pk)
    invite = Invite.objects.create(from_user=from_user, to_user=to_user)
    invite.save()
    return redirect('fbook:user_detail', pk=pk)


class OfferFriend(PageMixin, ListView):
    template_name = 'fbook/offer_friend.html'
    model = BookUser
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        current_user = BookUser.objects.get(pk=self.request.user.pk)
        return [user.from_user for user in current_user.to_user.all()]


@csrf_exempt
def accept_offer(request):
    if request.method == "POST" and request.is_ajax():
        current_user = BookUser.objects.get(pk=request.user.pk)
        pk_data = request.POST.get("pk")
        from_user = BookUser.objects.get(pk=pk_data)
        current_user.friend.add(from_user)
        from_user.friend.add(current_user)
        chat = Chat.objects.create(first_user=from_user, second_user=current_user)
        chat.save()
        from_user.save()
        current_user.save()
        Invite.objects.filter(from_user=from_user, to_user=current_user).delete()
        return JsonResponse({'name': 'Михаил'}, status=200)
    else:
        return HttpResponse('Не AJAX!')


class MyFriendList(PageMixin, ListView):
    template_name = 'fbook/my_friends.html'
    model = BookUser
    context_object_name = 'users'

    def get_queryset(self):
        current_user = BookUser.objects.get(pk=self.request.user.pk)
        return current_user.friend.all()


@login_required
def delete_friend(request, pk):
    try:
        current_user = BookUser.objects.get(pk=request.user.pk)
        user_to_delete = BookUser.objects.get(pk=pk)
        current_user.friend.remove(user_to_delete)
        user_to_delete.friend.remove(current_user)
        q = (Q(first_user=current_user) & Q(second_user=user_to_delete)) | (
                Q(first_user=user_to_delete) & Q(second_user=current_user))
        Chat.objects.filter(q).delete()
        current_user.save()
        user_to_delete.save()
        messages.add_message(request, messages.SUCCESS,
                             'Пользователь удален из друзей')
    except BookUser.DoesNotExist:
        return HttpResponseNotFound()
    return redirect('fbook:friends')


class ChatList(PageMixin, ListView):
    template_name = 'fbook/chats.html'
    model = BookUser
    context_object_name = 'users'

    def get_queryset(self):
        current_user = BookUser.objects.get(pk=self.request.user.pk)
        return current_user.friend.all()

    def get_context_data(self, **kwargs):
        current_user = BookUser.objects.get(pk=self.request.user.pk)
        data = super().get_context_data(**kwargs)
        users = self.get_queryset()
        data['flag_mes'] = []
        for user in users:
            q = (Q(first_user=current_user) & Q(second_user=user)) | (
                    Q(first_user=user) & Q(second_user=current_user))
            chat = Chat.objects.filter(q)[0]
            exist_messages = Message.objects.filter(chat=chat, author=user, is_active=True).exists()
            if exist_messages:
                data['flag_mes'].append(user.pk)

        return data


def chat_with_user(request, pk):
    current_user = BookUser.objects.get(pk=request.user.pk)
    user = get_object_or_404(BookUser, pk=pk)
    q = (Q(first_user=current_user) & Q(second_user=user)) | (
            Q(first_user=user) & Q(second_user=current_user))
    chat = Chat.objects.filter(q)[0]
    initial = {
        "chat": chat.pk,
        "author": current_user.pk,
    }
    form = SendMessageForm(initial=initial)
    if request.method == 'POST':
        c_form = SendMessageForm(request.POST)
        if c_form.is_valid():
            c_form.save()
        else:
            form = c_form
    current_messages = Message.objects.filter(chat=chat, author=current_user)
    user_messages = Message.objects.filter(chat=chat, author=user)
    for message in user_messages:
        message.is_active = False
        message.save()
    messages = current_messages.union(user_messages)
    context = {'form': form, 'all_messages': messages, 'to_user': user.pk}
    return render(request, 'fbook/chat_with_user.html', context)


@csrf_exempt
def like_handler(request):
    if request.method == "POST" and request.is_ajax():
        current_user = BookUser.objects.get(pk=request.user.pk)
        pk_data = request.POST.get("pk", None)
        try:
            post = Post.objects.get(pk=pk_data)
            if Like.objects.filter(from_user=current_user, post=post).exists():
                like = Like.objects.get(from_user=current_user, post=post)
                like.delete()
            else:
                like = Like.objects.create(from_user=current_user, post=post)
                like.save()
            count_likes = post.like_post.count()
            return JsonResponse({'count_likes': count_likes}, status=200)
        except Post.DoesNotExist:
            return HttpResponseNotFound()
    else:
        return HttpResponse('Не AJAX!')
