from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet)

auth_patterns = [
    path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]