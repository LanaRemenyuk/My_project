from django.contrib import admin

from .models import Tag, Material, Favorite, Follow, Price

EMPTY_VALUE = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = EMPTY_VALUE


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'measurement_unit')
    search_fields = ('amount',)
    list_filter = ('amount',)
    empty_value_display = EMPTY_VALUE


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date')
    search_fields = ('author', 'title', 'tags', 'price')
    # inlines = (AuthorMaterialInline,)
    empty_value_display = EMPTY_VALUE

    def is_favorited(self, obj):
        return Favorite.objects.filter(material=obj).count()

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('title')])


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'material')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user', )
    empty_value_display = EMPTY_VALUE
