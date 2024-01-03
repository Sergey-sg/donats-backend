from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import Jar, JarTag


@admin.register(Jar)
class JarAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'monobank_id', 'goal', 'date_added', 'dd_order']
    search_fields = ['monobank_id', 'title', 'tags']
    exclude = ['dd_order']
    ordering = ['dd_order', '-date_added']


@admin.register(JarTag)
class JarTagAdmin(admin.ModelAdmin):
    list_display = ['name']
