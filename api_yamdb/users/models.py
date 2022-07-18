from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import Roles


class UserProfile(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    role = models.CharField(
        choices=Roles.choices(),
        default='user',
        max_length=50,
        verbose_name='Роль'
    )
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.PositiveIntegerField(
        'Код подтверждения',
        default=0
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
