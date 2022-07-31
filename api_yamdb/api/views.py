from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genre, Titles
from users.permissions import IsAdminOrReadOnly
from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategoriesSerializer,
                          GenreSerializer,
                          TitlesSerializer,
                          TitlesPostSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitlesSerializer
        return TitlesPostSerializer
