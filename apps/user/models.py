from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField, CharField, URLField
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from .managers import CustomUserManager
from .validators import PHONE_REGEX


class User(AbstractUser):
    """
    User model
        attributes:
             email (str): used to log in the site
    """
    username = None
    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('used to login the site'),
        unique=True,
    )
    photo_profile = CloudinaryField(
        'photo_profile',
        folder='photo_profile',
        blank=True,
        null=True
    )
    photo_alt = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('photo_alt'),
        help_text=_('text to be loaded in case of image loss')
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


class VolunteerInfo(models.Model):
    """
    VolunteerInfo model
        attributes:
             user (class User): communication with the User model
             first_name (str): user first name
             last_name (str): user last name
             public_name (str): for display in donations and publication in articles
             additional_info (str): description of the volunteer's activities
             active (bool): active volunteer account or not
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('the user that the volunteer belongs to')
    )
    public_name = models.CharField(
        max_length=150,
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
        verbose_name=_('last name'),
        help_text=_('last name of the user')
    )
    phone_number = models.CharField(
        validators=[PHONE_REGEX],
        unique=True,
        max_length=13,
        null=True,
        blank=True,
        verbose_name=_('phone number'),
        help_text=_('The phone number must be in the format: "+380999999999"')
    )
    additional_info = models.TextField(
        verbose_name=_('additional info'),
        help_text=_('description of the volunteer\'s activities'),
        blank=True
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        help_text=_('active volunteer account or not'),
        default=False
    )

    class Meta:
        verbose_name = _('volunteer')
        verbose_name_plural = _('Volunteers')
        ordering = ['public_name']

    def __str__(self) -> CharField:
        """class method returns the volunteer in string representation"""
        return self.public_name


class LinkToSocial(models.Model):
    """
    LinkToSocial model
        attributes:
             volunteer (class VolunteerInfo): communication with the VolunteerInfo model
             link_to_social (str): a link to a social network
    """
    volunteer = models.ForeignKey(
        VolunteerInfo,
        on_delete=models.CASCADE,
        verbose_name=_('volunteer'),
        help_text=_('volunteer link owner')
    )
    link_to_social = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('link to social'),
        help_text=_('a link to a social network')
    )

    class Meta:
        verbose_name = _('Link to social')
        verbose_name_plural = _('Links to social')
        ordering = ['volunteer']

    def __str__(self) -> URLField:
        """class method returns the link to social in string representation"""
        return self.link_to_social
