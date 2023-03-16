from django.db import transaction

from drf_extra_fields.fields import Base64ImageField
from materials.models import Tag, Follow, Material, Favorite, ShoppingList, Price

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')

    @transaction.atomic
    def create(self, validated_data):
        user = super(CustomUserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'amount', 'measurement_unit')


class MaterialSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Material
        fields = ('id', 'tags', 'author', 'is_favorited',
                  'is_in_shopping_cart', 'title', 'file',
                  'description', 'pub_date', 'preview', 'price'
                  )

    def get_is_favorited(self, obj):
        return self._obj_exists(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self._obj_exists(obj, ShoppingList)

    def _obj_exists(self, recipe, name_class):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return name_class.objects.filter(user=request.user,
                                         recipe=recipe).exists()


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'title', 'preview', 'author', 'price', 'pub_date')


class FollowSerializer(CustomUserSerializer):
    materials = serializers.SerializerMethodField(read_only=True)
    materials_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'materials', 'materials_count',)

    def get_materials(self, obj):
        request = self.context.get('request')
        materials = obj.materials.all()
        materials_limit = request.query_params.get('materials_limit')
        if materials_limit:
            materials = materials[:int(materials_limit)]
        return MaterialListSerializer(materials, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class FavoriteSerializer(MaterialListSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'material')

    def to_representation(self, instance):
        return representation(
            self.context,
            instance.material,
            MaterialListSerializer)


class ShoppingListSerializer(MaterialListSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'material')

    def to_representation(self, instance):
        return representation(
            self.context,
            instance.material,
            MaterialListSerializer)


def representation(context, instance, serializer):
    request = context.get('request')
    new_context = {'request': request}
    return serializer(instance, context=new_context).data