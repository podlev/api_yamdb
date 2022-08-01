from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Titles, Genre, Categories, Review, Comments
from rest_framework import serializers
# from django.db.models import Avg
import datetime as dt


class TitlesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Titles для записи данных"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories"""

    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Titles для чтения данных"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    # rating = serializers.IntegerField(
    #     Titles.objects.annotate(rating=Avg('reviews__score'))
    # )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


        def validate_year(self, value):
            year = dt.date.today().year
            if not value <= year:
                raise serializers.ValidationError(
                    'Проверьте год издания произведения!')
            return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    # class Meta:
    #     model = Review
    #     fields = ('author', 'title')
    #     validators = [
    #         serializers.UniqueTogetherValidator(
    #             queryset=Review.objects.all(),
    #             fields=['review', 'title'],
    #             message='Невозможно добавить более '
    #                     'одного отзыва на произведение'
    #         )
    #     ]

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более '
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
