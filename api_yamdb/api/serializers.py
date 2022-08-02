from django.db import models
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Title, Genre, Categories, Review, Comments
from rest_framework import serializers
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
        model = Title
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
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']



    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',
                  'rating')

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

    def validate(self, ser_data):
        author = None
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            author = request.user
        if author.id:
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if (request.method == 'POST'
                    and Review.objects.filter(title=title,
                                              author=author).exists()):
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв')
            return ser_data

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
