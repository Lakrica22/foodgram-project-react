from http import HTTPStatus
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Ingredient, Recipe, Tag
from .filters import IngredientSearchFilter, RecipeFilter
from .serializers import (IngredientSerializer, FavoriteSerializer,
                          RecipeSerializer, RecipeSerializerCreate,
                          ShoppingCartSerializer, TagSerializer)
from recipes.models import ShoppingCart, Favorite, IngredientRecipe


class TagsViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с тегами.
    """
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с ингридиентами.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientSearchFilter]


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с рецептами.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_class = RecipeFilter
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipeSerializerCreate

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)


class BaseFavoriteCartViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class CartViewSet(BaseFavoriteCartViewSet):

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart


class FavoriteViewSet(BaseFavoriteCartViewSet):

    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite


class DownloadCartView(APIView):

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def get(self, request):
        user = request.user
        if not user.carts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
