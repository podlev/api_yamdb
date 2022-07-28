from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
    role = models.CharField(choices=ROLE_CHOICES, default='user', max_length=10)
