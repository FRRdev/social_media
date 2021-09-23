from django.contrib.auth.backends import ModelBackend
from .models import BookUser


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = BookUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                return None
        except BookUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BookUser.objects.get(pk=user_id)
        except BookUser.DoesNotExist:
            return None
