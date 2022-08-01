from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.views import (CategoriesViewSet, GenreViewSet,
                       TitlesViewSet, CommentsViewSet, ReviewViewSet)

router = DefaultRouter()

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentsViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]