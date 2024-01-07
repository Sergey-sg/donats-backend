from cloudinary.models import CloudinaryField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..user.models import VolunteerInfo


class JarTag(models.Model):
    """
    Jar tag model

    Fields:
        - name (str): jar tag name
    """
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        verbose_name=_('name'),
        help_text=_('The name of tag'),
        unique=True
    )

    class Meta:
        verbose_name = _('jar tag')
        verbose_name_plural = _('Jar Tags')
        ordering = ['name']

    def __str__(self) -> str:
        """class method returns the tag in string representation"""
        return self.name


class Jar(models.Model):
    """
    Model for representing Jars with associated details.

    Fields:
        - `monobank_id` (str): ID of the monobank jar.
        - `title` (str): Name of the jar specified by the user.
        - `volunteer` (VolunteerInfo): Reference to the volunteer to whom the jar belongs.
        - `tags` (ManyToManyField[JarTag]): Tags associated with the jar.
        - `goal` (PositiveIntegerField): A goal sum of the jar.
        - `title_img` (CloudinaryField): Cloudinary field for the title image of the jar.
        - `img_alt` (str): Text to be loaded in case of image loss.
        - `date_added` (DateTimeField): The date and time when the jar was added to the website.
        - `date_closed` (DateTimeField): The date and time when the goal sum in the jar was reached.
        - `dd_order` (PositiveIntegerField): Default ordering field.
    """
    monobank_id = models.CharField(
        max_length=31,
        validators=[MinLengthValidator(10)],
        verbose_name=_('monobank jar id'),
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
        VolunteerInfo,
        on_delete=models.CASCADE,
        verbose_name=_('volunteer'),
        help_text=_('Reference to volunteer to who jar belongs'),
    )
    tags = models.ManyToManyField(
        to=JarTag,
        verbose_name=_('tags'),
        help_text=_('Tags for Jar'),
        blank=True
    )
    goal = models.PositiveIntegerField(
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
        help_text=_('Text to be loaded in case of image loss')
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

    class Meta:
        verbose_name = _('jar')
        verbose_name_plural = _('Jars')
        ordering = ['-date_added']

    def __str__(self) -> str:
        """class method returns the Jar in string representation"""
        return self.title


class AmountOfJar(models.Model):
    """
    Amount of jar model
        Fields:
            sum (int): jar current sum
            jar (Jar): foreign key to jar which sum is represented
            date_added (date): date when amount was added
    """
    sum = models.PositiveIntegerField(
        verbose_name=_('sum'),
        help_text=_('A current sum in jar'),
        null=True,
        blank=True
    )
    jar = models.ForeignKey(
        Jar,
        on_delete=models.CASCADE,
        verbose_name=_('jar'),
        help_text=_('The Jar that the AmountOfJar belongs to'),
    )
    date_added = models.DateField(
        auto_now_add=True,
        verbose_name=_('date added'),
        help_text=_('The date and time when sum was added.')
    )

    class Meta:
        verbose_name = _('amount of jar')
        verbose_name_plural = _('Amounts Of Jars')
        ordering = ['jar', '-date_added']

    def __str__(self) -> str:
        """class method returns the amount in string representation"""
        return f'{self.sum}'


class JarAlbum(models.Model):
    """
    Model for representing albums of images associated with Jars.

    Fields:
    - `jar` (Jar): The Jar that the images of JarAlbum belongs to.
    - `img` (CloudinaryField): Cloudinary field for the image of the album.
    - `img_alt` (str): Text to be loaded in case of image loss.
    - `date_added` (DateField): The date when the image was added to the album.
    """
    jar = models.ForeignKey(
        Jar,
        on_delete=models.CASCADE,
        verbose_name=_('jar'),
        help_text=_('The Jar that the images of JarAlbum belongs to')
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
        ordering = ['date_added']

    def __str__(self) -> str:
        """class method returns the image URL in string representation."""
        return f'{self.img}'
