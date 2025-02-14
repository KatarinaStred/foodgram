from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers


from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('docs/', TemplateView.as_view(template_name='docs/redoc.html'),
         name='redoc'),
    path('auth/', include('djoser.urls.authtoken')),
]
