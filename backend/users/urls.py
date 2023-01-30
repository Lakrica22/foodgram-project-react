from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, SubscriptionListView, SubscriptionViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

auth_patterns = [
    path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionViewSet.as_view(),
        name='subscribe'
    ),
    path('auth/', include(auth_patterns)),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
