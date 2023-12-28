from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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
             tags (str): list of tags separated by comma
             goal (int): the goal sum of jar
             current (int): the current sum in jar
             active (bool): show whether jar is still active
             date_added (date): date when jar was added to application
             date_closed (date): The date and time when goal sum in jar was reached.
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
    active = models.BooleanField(default=False)
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date added'),
        help_text=_('The date and time when jar was added to website.'),
    )
    date_closed = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('date closed'),
        help_text=_('The date and time when goal sum in jar was reached.'),
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
