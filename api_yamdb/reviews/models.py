from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


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
    year = models.PositiveSmallIntegerField('Год создания')
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
    title_id = models.ForeignKey(Titles, on_delete=models.CASCADE, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)


class Review(models.Model):
    """Модель рейтинга произведений"""
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comments(models.Model):
    """Модель комментариев к произведениям"""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'