from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models

from api.constants import (
    MAX_NAME_LENGTH,
    MAX_NAME_ING_LENGTH,
    MAX_TAG_LENGTH,
    MAX_UNIT_ING_LENGTH,
    MIN_VALUE_VALID,
    REGEX_SLUG
)


User = get_user_model()


class Tag(models.Model):
    """Описание модели тегов."""

    name = models.CharField(
        max_length=MAX_TAG_LENGTH,
        unique=True,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=MAX_TAG_LENGTH,
        unique=True,
        verbose_name='Slug тега',
        validators=[validators.RegexValidator(
                    regex=REGEX_SLUG,
                    message='Недопустимый slug!')]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Описание модели ингредиентов."""

    name = models.CharField(
        max_length=MAX_NAME_ING_LENGTH,
        verbose_name='Наименование ингредиента',
        blank=False,
        null=False
    )
    measurement_unit = models.CharField(
        max_length=MAX_UNIT_ING_LENGTH,
        verbose_name='Единица измерения',
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Описание модели рецептов."""

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes'
    )
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Название рецепта',
        unique=True
    )
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(MIN_VALUE_VALID)],
        help_text='Время приготовления (в минутах)'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        ordering = ['-id']

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Описание модели списка покупок."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        default_related_name = 'shopping_cart'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart')]

    def __str__(self):
        return (
            f'Рецепт {self.recipe}'
            f' добавлен в список покупок пользователя {self.user}')


class Favorite(models.Model):
    """Описание модели избранного."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite')]

    def __str__(self):
        return (
            f'Рецепт {self.recipe}'
            f' добавлен в избранное пользователя {self.user}')


class IngredientInRecipe(models.Model):
    """Описание модели связи ингредиентов с рецептом."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиентов',
        validators=[MinValueValidator(MIN_VALUE_VALID)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        default_related_name = 'ingredient_in_recipes'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_in_recipe')]

    def __str__(self):
        return (
            f'Ингредиент {self.ingredient}'
            f' в кол-ве: {self.amount}'
            f' добавлен в рецепт {self.recipe}')
