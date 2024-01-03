from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainPageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.jars'
    verbose_name = _('Jars list')
