from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models

from fbook.models import BookUser, Post, Chat
from .serializer import BookUserListSerializer, BookUserDetailSerializer, CommentCreateSerializer, PostDetailSerializer, \
    CreateMessageSerializer, ChatSerializer


class BookUserListView(generics.ListAPIView):
    serializer_class = BookUserListSerializer
    queryset = BookUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class BookUserDetailView(APIView):
    def get(self, request, pk):
        user = BookUser.objects.get(pk=pk)
        serializer = BookUserDetailSerializer(user)
        return Response(serializer.data)


class CommentCreateView(APIView):
    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)


class PostDetailView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class AddMessageView(APIView):
    def post(self, request):
        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)


class ChatDetailView(APIView):
    def get(self, request, pk):
        chat = Chat.objects.get(pk=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
