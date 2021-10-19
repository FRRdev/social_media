from rest_framework import serializers

from fbook.models import BookUser, Comment, Post, Message, Chat


class BookUserListSerializer(serializers.ModelSerializer):
    friend = serializers.SlugRelatedField(slug_field='email', read_only=True, many=True)
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


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("author", "chat", "content")

    def create(self, validated_data):
        message = Message.objects.update_or_create(
            author=validated_data.get('author', None),
            chat=validated_data.get('chat'),
            content=validated_data.get('content', None),
            defaults={'content': validated_data.get('content')}
        )
        return message


class ChatSerializer(serializers.ModelSerializer):
    first_user = BookUserDetailSerializer(many=False)
    second_user = BookUserDetailSerializer(many=False)

    class Meta:
        model = Chat
        fields = '__all__'
