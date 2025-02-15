from django.contrib import admin
from recipes.models import (
    Ingredient,
    IngredientInRecipe,
    Favorite,
    Recipe,
    ShoppingCart,
    Tag
)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe


class ShoppingCartInline(admin.StackedInline):
    model = ShoppingCart


class FavoriteInline(admin.StackedInline):
    model = Favorite


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInRecipeInline,
    )

    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInRecipeInline,
        FavoriteInline,
        ShoppingCartInline,
    )

    list_display = ('name', 'author', 'in_favorite')
    list_display_links = ('name',)
    fields = ('name', 'author', 'text', 'tags')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)

    @admin.display(description='Добавлено в избранное')
    def in_favorite(self, obj):
        return f'{obj.favorites.count()} польз.'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass
