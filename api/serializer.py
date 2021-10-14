from rest_framework import serializers

from fbook.models import BookUser


class BookUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = ('first_name', 'last_name', 'email', 'friend')


class BookUserDetailSerializer(serializers.ModelSerializer):
    friend = serializers.SlugRelatedField(slug_field='email', read_only=True, many=True)

    class Meta:
        model = BookUser
        fields = ('first_name', 'last_name', 'email', 'image', 'phone', 'date_of_birth', 'city', 'about_me', 'friend')
