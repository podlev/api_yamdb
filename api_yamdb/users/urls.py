from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, new_user, update_token

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', new_user),
    path('api/v1/auth/token/', update_token)
]
