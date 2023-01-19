from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet, SubscriptionListView, SubscriptionViewSet
from .views import IngredientViewSet, DownloadCartView, RecipeViewSet, TagsViewSet, FavoriteViewSet, CartViewSet

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
        SubscriptionViewSet.as_view(),
        name='subscribe'
    ),
    path('recipes/download_shopping_cart/',
         DownloadCartView.as_view(), name='download_shopping_cart'),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)), 
]
