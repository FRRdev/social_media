from rest_framework.response import Response
from rest_framework.views import APIView

from fbook.models import BookUser
from .serializer import BookUserListSerializer, BookUserDetailSerializer


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
