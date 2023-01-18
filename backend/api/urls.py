from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet, SubscriptionListView, SubscriptionSerializer
from .views import IngredientViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionSerializer.as_view(),
        name='subscribe'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)), 
]
