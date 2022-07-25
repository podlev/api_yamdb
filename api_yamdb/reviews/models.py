from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Titles(models.Model):
    pass


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Genres(models.Model):
    pass


class Genre_title(models.Model):
    pass
