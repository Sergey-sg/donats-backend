from django.contrib import admin

from .models import Jar, JarTag


@admin.register(Jar)
class JarAdmin(admin.ModelAdmin):
    list_display = ['title', 'monobank_id', 'goal', 'current', 'date_added']
    search_fields = ['monobank_id', 'title', 'tags']
    ordering = ['-date_added']


@admin.register(JarTag)
class JarTagAdmin(admin.ModelAdmin):
    list_display = ['name']
