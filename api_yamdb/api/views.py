from rest_framework import viewsets

from reviews.models import Categories, Genre, Titles
from .serializers import (CategoriesSerializer,
                          GenreSerializer,
                            TitlesSerializer)
from .mixins import ListCreateDestroyViewSet


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

    # def get_serializer_class(self):


