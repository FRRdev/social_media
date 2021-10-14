from rest_framework.response import Response
from rest_framework.views import APIView

from fbook.models import BookUser,Post
from .serializer import BookUserListSerializer, BookUserDetailSerializer, CommentCreateSerializer,PostDetailSerializer


class BookUserListView(APIView):
    def get(self, request):
        users = BookUser.objects.all()
        serializer = BookUserListSerializer(users, many=True)
        return Response(serializer.data)


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
