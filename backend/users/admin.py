from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.models import Favorite
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'favorite_count',
        'avatar')
    list_filter = ('email', 'first_name')
    empty_value_display = '-empty-'

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author')
    search_fields = ('user', 'author')
    empty_value_display = '-empty-'
