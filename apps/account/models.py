from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from .managers import CustomUserManager


class User(AbstractUser):
    """
    User model
        attributes:
             first_name (str): user first name
             last_name (str): user last name
             email (str): used to log in the site
             public_name (str): for display in donations and publication in articles
    """
    username = None
    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('used to login the site'),
        unique=True,
    )
    public_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('public name'),
        help_text=_('for display in donations and publication in articles')
    )
    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('first name'),
        help_text=_('first name of the user')
    )
    last_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('first name'),
        help_text=_('last name of the user')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')
        ordering = ['email']

    def __str__(self) -> EmailField:
        """class method returns the user in string representation"""
        return self.email
