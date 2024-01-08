from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Jar, JarAlbum
from shared.cloudinary.utils import image_pre_save, delete_cloudinary_image


@receiver(pre_save, sender=Jar)
def delete_old_title_img(sender, instance, **kwargs):
    """Deletes the old image from Cloudinary if it has changed"""
    image_pre_save(sender, instance, field_name='title_img')


@receiver(pre_delete, sender=Jar)
def delete_title_img(sender, instance, **kwargs):
    """Delete the image from Cloudinary before deleting the Jar"""
    old_instance = sender.objects.get(pk=instance.pk)
    delete_cloudinary_image(old_instance, field_name='title_img')


@receiver(pre_save, sender=JarAlbum)
def delete_old_img(sender, instance, **kwargs):
    """Deletes the old image from Cloudinary if it has changed"""
    image_pre_save(sender, instance, field_name='img')


@receiver(pre_delete, sender=JarAlbum)
def delete_img(sender, instance, **kwargs):
    """Delete the image from Cloudinary before deleting the JarAlbum"""
    old_instance = sender.objects.get(pk=instance.pk)
    delete_cloudinary_image(old_instance, field_name='img')
