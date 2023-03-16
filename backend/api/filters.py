from django_filters.rest_framework import FilterSet, filters
from materials.models import Material, Tag


class MaterialFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Material
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')