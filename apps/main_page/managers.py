from django.db import models
from django.utils import text


class JarManager(models.Manager):
    def create_jar(self, monobank_id, title, **extra_fields):
        title = text.capfirst(title)
        jar = self.model(monobank_id=monobank_id, title=title, **extra_fields)
        jar.save()
        return jar


class JarTagManager(models.Manager):
    def create_tag(self, name):
        name = name.lower()
        tag = self.model(name=name)
        tag.save()
        return tag
