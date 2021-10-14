from rest_framework import serializers

from fbook.models import BookUser, Comment, Post


class BookUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = ('first_name', 'last_name', 'email', 'friend')


class BookUserDetailSerializer(serializers.ModelSerializer):
    friend = serializers.SlugRelatedField(slug_field='email', read_only=True, many=True)

    class Meta:
        model = BookUser
        fields = ('first_name', 'last_name', 'email', 'image', 'phone', 'date_of_birth', 'city', 'about_me', 'friend')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Comment
        exclude = ('post',)


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    cmnts = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
