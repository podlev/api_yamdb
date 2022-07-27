from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import (CategoriesViewSet, GenreViewSet, TitlesViewSet)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
