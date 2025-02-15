from django.core.exceptions import ValidationError
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.http import require_GET
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.filters import IngredientFilter, RecipesFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AvatarSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    PasswordSerializer,
    RecipeEditSerializer,
    RecipeReadSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    SubscriptionUserSerializer,
    TagSerializer,
    UserSerializer)
from recipes.models import (
    Ingredient,
    IngredientInRecipe,
    Favorite,
    Recipe,
    ShoppingCart,
    Tag)
from users.models import Subscription, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра ингредиентов."""

    queryset = Ingredient.objects.all()
    model = Ingredient
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = RecipesFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return RecipeReadSerializer
        return RecipeEditSerializer

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[AllowAny],
        url_path='get-link',
        url_name='get-link'
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        rev_link = reverse('get_short_link', args=[recipe.pk])
        return Response({'short-link': request.build_absolute_uri(rev_link)},
                        status=status.HTTP_200_OK,)

    def check_recipe_action(self, request, model, serializer_class):
        recipe = self.get_object()
        user = request.user
        if request.method == 'POST':
            obj, created = model.objects.get_or_create(
                user=user,
                recipe=recipe)
            if not created:
                return Response(
                    {'detail': 'Такой рецепт уже есть!'},
                    status=status.HTTP_400_BAD_REQUEST)
            data = serializer_class(recipe, context={'request': request}).data
            return Response(data, status=status.HTTP_201_CREATED)

        obj = model.objects.filter(user=user, recipe=recipe).first()
        if not obj:
            return Response(
                {'detail': 'Рецепт не найден.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.check_recipe_action(
            request,
            Favorite,
            FavoriteSerializer)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.check_recipe_action(
            request,
            ShoppingCart,
            ShoppingCartSerializer)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.filter(shopping_cart__user=request.user)
        shopping_cart = IngredientInRecipe.objects.filter(
            recipe__in=recipes).values(
            name=F('ingredient__name'),
            units=F('ingredient__measurement_unit')).order_by(
            'ingredient__name').annotate(total=Sum('amount'))
        text = 'Список покупок: \n\n'
        ingr_list = []
        for recipe in shopping_cart:
            ingr_list.append(recipe)
        for i in ingr_list:
            text += f'{i["name"]}: {i["total"]}, {i["units"]}.\n'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.txt"')
        return response


@require_GET
def get_short_link(request, pk):
    try:
        Recipe.objects.filter(pk=pk).exists()
        return redirect(f'/recipes/{pk}/')
    except Exception:
        raise ValidationError(f'Рецепт с id "{pk}" не найден.')


class UserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['POST'])
    def set_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.data.get('current_password')):
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Пароль указан неверно!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['PUT'],
        permission_classes=[IsAuthorOrReadOnly],
        url_path='me/avatar',
    )
    def avatar(self, request, *args, **kwargs):
        serializer = AvatarSerializer(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request, *args, **kwargs):
        user = self.request.user
        user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if request.user == author:
                return Response({
                    'detail': 'Нельзя подписаться на самого себя.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response({
                    'detail': 'Подписка уже есть.'
                }, status=status.HTTP_400_BAD_REQUEST)
            new_subscript = Subscription.objects.create(
                user=user,
                author=author)
            serializer = SubscriptionSerializer(
                new_subscript,
                context={'request': request})
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Subscription,
                user=user,
                author=author)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following_author__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionUserSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
