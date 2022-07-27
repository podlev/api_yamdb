from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    """Модель категорий произведений"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Модель жанров произведений"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Titles(models.Model):
    """Модель произведений"""
    name = models.CharField(max_length=50)
    year = models.DateTimeField('Год создания')
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='Genre_title')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Genre_title(models.Model):
    """Вспомогательная модель жанров произведений"""
    title_id = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


