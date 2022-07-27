from rest_framework.routers import DefaultRouter

from django.urls import include, path
from .views import (CategoriesViewSet,
GenreViewSet, CategoriesSerializer)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', CategoriesSerializer, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
