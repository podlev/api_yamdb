from reviews.models import Titles, Genre, Categories
from rest_framework import serializers


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
