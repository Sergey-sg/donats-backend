from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import apps.user.models
from apps.jars.managers import JarManager, JarTagManager


class JarTag(models.Model):
    """
        Jar tag model
            attributes:
                 name (str): jar tag name
    """
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        verbose_name=_('name'),
        help_text=_('The name of tag'),
        unique=True
    )

    objects = JarTagManager()

    class Meta:
        verbose_name = _('jar tag')
        verbose_name_plural = _('jar tags')
        ordering = ['name']

    def __str__(self):
        return self.name


class Jar(models.Model):
    """
    Jar model
        attributes:
             monobank_id (str): jar id in monobank
             title (str): jar title
             volunteer (bigint): reference to volunteer owner
             tags (str): list of tags separated by comma
             goal (int): the goal sum of jar
             active (bool): show whether jar is still active
             date_added (date): date when jar was added to application
             date_closed (date): The date and time when goal sum in jar was reached
             dd_order (int): used to drag and drop items in the admin
    """
    monobank_id = models.CharField(
        max_length=31,
        validators=[MinLengthValidator(10)],
        verbose_name=_('jar id'),
        help_text=_('ID of monobank jar'),
        unique=True
    )
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        verbose_name=_('jar name'),
        help_text=_('Name of jar specified by user'),
    )
    volunteer = models.ForeignKey(
        apps.user.models.VolunteerInfo,
        on_delete=models.CASCADE,
        verbose_name=_('volunteer'),
        help_text=_('Reference to volunteer to who jar belongs'),
    )
    tags = models.ManyToManyField(
        to=JarTag
    )
    goal = models.IntegerField(
        validators=[MinValueValidator(0, 'Value can\'t be less than 0')],
        verbose_name=_('goal'),
        help_text=_('A goal sum of jar'),
        null=True,
        blank=True
    )
    title_img = CloudinaryField(
        'title_img',
        folder='jar_title_img',
        blank=True,
        null=True
    )
    img_alt = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('img_alt'),
        help_text=_('text to be loaded in case of image loss')
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date added'),
        help_text=_('The date and time when jar was added to website.'),
    )
    date_closed = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name=_('date closed'),
        help_text=_('The date and time when goal sum in jar was reached.'),
    )
    dd_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False
    )

    objects = JarManager()

    class Meta:
        verbose_name = _('jar')
        verbose_name_plural = _('jars')
        ordering = ['-date_added']

    def __str__(self):
        return self.title


class JarCurrentSum(models.Model):
    """
        Jar current sum model
            attributes:
                 sum (int): jar current sum
                 jar (bigint): foreign key to jar which sum is represented
    """
    sum = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text=_('A current sum in jar')
    )
    jar = models.ForeignKey(
        Jar,
        on_delete=models.CASCADE,
        verbose_name=_('jar id'),
    )
    date_added = models.DateField(
        auto_now_add=True,
        verbose_name=_('date added'),
        help_text=_('The date and time when sum was added to db.')
    )

    class Meta:
        verbose_name = _('jar current sum')
        verbose_name_plural = _('jar current sums')
        ordering = ['sum']

    def __str__(self):
        return self.sum


class JarAlbum(models.Model):
    """
   JarAlbum model for managing albums associated with jars.

   Attributes:
       - `jar` (Jar): ForeignKey to the Jar model, indicating the jar to which the album belongs.
       - `img` (CloudinaryField): CloudinaryField for storing images associated with the jar album.
       - `img_alt` (str): A short text to be loaded in case of image loss.
       - `date_added` (date): The date when the album was added, updated automatically.

   Example:
   ```
   {
       "jar": 1,
       "img": "<cloudinary_url>",
       "img_alt": "Alternative text",
       "date_added": "2024-01-02"
   }
   ```

   Fields:
       - `jar` (required): ForeignKey to the associated Jar model.
       - `img` (required): CloudinaryField for storing images associated with the jar album.
       - `img_alt` (optional): A short text to be loaded in case of image loss.
       - `date_added` (automatic): The date when the album was added, updated automatically.

   Usage:
       - Each instance of this model represents an album associated with a specific jar.
   """
    jar = models.ForeignKey(
        Jar,
        on_delete=models.CASCADE,
        verbose_name=_('jar'),
        help_text=_('The jar that the jar album belongs to')
    )
    img = CloudinaryField(
        'img',
        folder='jar_album',
        blank=True,
        null=True
    )
    img_alt = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_('img_alt'),
        help_text=_('text to be loaded in case of image loss')
    )
    date_added = models.DateField(auto_now=True, verbose_name=_('date added'))

    class Meta:
        verbose_name = _('jar album')
        verbose_name_plural = _('Albums of jars')
        ordering = ['-date_added']

    def __str__(self) -> str:
        """class method returns the JarAlbum in string representation"""
        return f'{self.img}'
