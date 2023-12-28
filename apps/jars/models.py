from django.core.validators import MinValueValidator
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
        validators=[MinValueValidator(2)],
        verbose_name=_('name'),
        help_text=_('The name of tag')
    )

    objects = JarTagManager()

    class Meta:
        verbose_name = _('jar tag')
        verbose_name_plural = _('jar tags')
        ordering = ['name']


class Jar(models.Model):
    """
    Jar model
        attributes:
             monobank_id (str): jar id in monobank
             title (str): jar title
             tags (str): list of tags separated by comma
             goal (int): the goal sum of jar
             current (int): the current sum in jar
             date_added (date): date when jar was added to application
    """
    monobank_id = models.CharField(
        max_length=11,
        validators=[MinValueValidator(10)],
        verbose_name=_('jar id'),
        help_text=_('ID of monobank jar')
    )
    title = models.CharField(
        max_length=50,
        validators=[MinValueValidator(1)],
        verbose_name=_('jar name'),
        help_text=_('Name of jar specified by user')
    )
    tags = models.ManyToManyField(
        to=JarTag
    )
    goal = models.IntegerField(
        validators=[MinValueValidator(0, 'Value can\'t be less than 0')],
        verbose_name=_('goal'),
        help_text=_('A goal sum of jar')
    )
    current = models.IntegerField(
        validators=[MinValueValidator(0, 'Value can\'t be less than 0')],
        verbose_name=_('current'),
        help_text=_('A current sum in jar')
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    objects = JarManager()

    class Meta:
        verbose_name = _('jar')
        verbose_name_plural = _('jars')
        ordering = ['-date_added', 'current']

    def __str__(self):
        return self.title
