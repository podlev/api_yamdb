from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с ролями"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True, default='')
    role = models.CharField(choices=ROLE_CHOICES,
                            default='user',
                            max_length=10)

    def save(self, *args, **kwargs):
        """При сохранении в поле роль ставит admin если это супер юзер"""
        if self.is_superuser:
            self.role = 'admin'
        super(User, self).save()

    def __str__(self):
        return f'User: {self.username}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
