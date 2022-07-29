import django_filters
from reviews.models import Titles

class TitlesFilter(django_filters.rest_framework.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='contains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='contains'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )
    class Meta:
        model = Titles
        fields = ['genre__slug', 'category__slug', 'name']


