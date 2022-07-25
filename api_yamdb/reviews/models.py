from django.db import models

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


