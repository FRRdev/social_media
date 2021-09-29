from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class BookUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20, db_index=True, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия пользователя')
    email = models.EmailField(null=True, blank=True, verbose_name='почта', unique=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Изображение')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    date_of_birth = models.DateField(max_length=8, null=True, blank=True, verbose_name='Дата рождения')
    city = models.CharField(max_length=20, null=True, blank=True, verbose_name='Город')
    about_me = models.TextField(max_length=500, null=True, blank=True, verbose_name='Обо мне')
    friend = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='Друзья', default=[],
                                    related_name='friends')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['first_name']


class Post(models.Model):
    title = models.TextField(max_length=150)
    text = models.TextField(verbose_name='текст')
    user = models.ForeignKey(BookUser, on_delete=models.CASCADE, verbose_name='пользователь', related_name='posts')
    create_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-create_at']

    def __str__(self):
        return f'Пост {self.id}'


class Comment(models.Model):
    author = models.ForeignKey(BookUser, on_delete=models.CASCADE, verbose_name='пользователь')
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['author']


class Chat(models.Model):
    first_user = models.OneToOneField(BookUser, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.OneToOneField(BookUser, on_delete=models.CASCADE, related_name='second_user')

    class Meta:
        verbose_name_plural = 'Чаты'
        verbose_name = 'Чат'

    def __str__(self):
        return f'Чат между {self.first_user} и {self.second_user}'


class Message(models.Model):
    author = models.ForeignKey(BookUser, on_delete=models.CASCADE, verbose_name='автор')
    create_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    content = models.TextField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
        ordering = ['author']

    def __str__(self):
        return f'сообщение - {self.id}'


class Invite(models.Model):
    from_user = models.ForeignKey(BookUser, on_delete=models.PROTECT, related_name='from_user', unique=False)
    to_user = models.ForeignKey(BookUser, on_delete=models.PROTECT, related_name='to_user', unique=False)

    class Meta:
        verbose_name_plural = 'Приглашения'
        verbose_name = 'Пригляшение'

    def __str__(self):
        return f'Приглашение от {self.from_user} к {self.to_user}'


class Like(models.Model):
    from_user = models.OneToOneField(BookUser, on_delete=models.PROTECT)
    post = models.OneToOneField(Post, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Лайки'
        verbose_name = 'Лайк'

    def __str__(self):
        return f'Лайк от {self.from_user} к {self.post}'

