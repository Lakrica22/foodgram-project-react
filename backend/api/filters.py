from django_filters.rest_framework import FilterSet, filters, CharFilter
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe


class IngredientsFilter(FilterSet):
    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    """
    Фильтр для сортировки рецептов по:
    тегам, нахождению в избранном и корзине.
    """
    tags = filters.AllValuesMultipleFilter(field_name='tags')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    #def filter_is_favorited(self, queryset, name, value):
    #    if value:
    #        return queryset.filter(favourites=self.request.user)
    #    return queryset
    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favourites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset
