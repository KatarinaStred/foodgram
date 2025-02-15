from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from api.constants import (
    MAX_EMAIL_LENGTH,
    MAX_USER_LENGTH,
    REGEX_USERNAME
)


class User(AbstractUser):
    """Описание модели пользователя."""

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        verbose_name='Адрес электронной почты',
        unique=True
    )
    username = models.CharField(
        max_length=MAX_USER_LENGTH,
        verbose_name='Уникальный юзернейм',
        unique=True,
        validators=[
            MaxLengthValidator(MAX_USER_LENGTH),
            RegexValidator(REGEX_USERNAME)
        ]
    )
    first_name = models.CharField(
        max_length=MAX_USER_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_USER_LENGTH,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        default=None,
        upload_to='media/avatars/',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'avatar']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Описание модели подписки."""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following_author',
        default=None
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow')]

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя!')

    def __str__(self):
        return (
            f'Пользователь {self.user.username}'
            f' подписан на {self.author.username}.')
