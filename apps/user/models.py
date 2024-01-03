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
    User model for the application.

    Attributes:
        - `email` (str): Email address used for logging into the site.
        - `photo_profile` (CloudinaryField): Cloudinary field for storing the user's profile photo.
        - `photo_alt` (str): Text to be displayed in case of image loss for the profile photo.

    Example:
    ```
    {
        "email": "user@example.com",
        "photo_profile": "<cloudinary_url>",
        "photo_alt": "User's profile photo"
    }
    ```

    Fields:
        - `email` (required): The email address used for logging in (unique).
        - `photo_profile` (optional): The Cloudinary URL for the user's profile photo.
        - `photo_alt` (optional): Text to be displayed in case the profile photo is not available.
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
    VolunteerInfo model for managing volunteer information.

    Attributes:
        - `user` (User): One-to-one relationship with the User model.
        - `public_name` (str): Name for display in donations and publication in articles.
        - `first_name` (str): First name of the volunteer.
        - `last_name` (str): Last name of the volunteer.
        - `phone_number` (str): Phone number of the volunteer (optional).
        - `additional_info` (str): Description of the volunteer's activities.
        - `active` (bool): Indicates whether the volunteer account is active.

    Example:
    ```
    {
        "user": {
            "email": "volunteer@example.com",
            "photo_profile": "<cloudinary_url>",
            "photo_alt": "Volunteer's profile photo"
        },
        "public_name": "JohnDoe",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+380999999999",
        "additional_info": "Passionate about community service.",
        "active": True
    }
    ```

    Fields:
        - `user` (required): The associated User model.
        - `public_name` (required): Name for display in donations and publication in articles.
        - `first_name` (required): First name of the volunteer.
        - `last_name` (required): Last name of the volunteer.
        - `phone_number` (optional): Phone number of the volunteer (in the format: "+380999999999").
        - `additional_info` (optional): Description of the volunteer's activities.
        - `active` (optional): Indicates whether the volunteer account is active.

    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('The user that the volunteer belongs to')
    )
    public_name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(3)],
        verbose_name=_('public name'),
        help_text=_('For display in donations and publication in articles')
    )
    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('first name'),
        help_text=_('First name of the user')
    )
    last_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name=_('last name'),
        help_text=_('Last name of the user')
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
        help_text=_('Description of the volunteer\'s activities'),
        blank=True
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        help_text=_('Active volunteer account or not'),
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
    LinkToSocial model for managing links to social networks.

    Attributes:
        - `volunteer` (VolunteerInfo): ForeignKey relationship with the VolunteerInfo model.
        - `link_to_social` (str): A link to a social network.

    Example:
    ```
    {
        "volunteer": {
            "user": {
                "email": "volunteer@example.com",
                "photo_profile": "<cloudinary_url>",
                "photo_alt": "Volunteer's profile photo"
            },
            "public_name": "JohnDoe",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+380999999999",
            "additional_info": "Passionate about community service.",
            "active": true
        },
        "link_to_social": "https://www.linkedin.com/in/johndoe/"
    }
    ```

    Fields:
        - `volunteer` (required): The associated VolunteerInfo model.
        - `link_to_social` (optional): A link to a social network.

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
