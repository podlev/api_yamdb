<<<<<<< HEAD
from django.db import models

=======
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Titles(models.Model):
    pass


>>>>>>> f263828a5f6f75f0c8573330f527961c6cffb933
class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=50)
    year = models.DateTimeField('Год создания')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Genre_title(models.Model):
    title_id = models.


