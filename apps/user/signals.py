from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from shared.cloudinary.utils import image_pre_save, delete_cloudinary_image
from .models import User


@receiver(pre_save, sender=User)
def delete_old_profile_picture(sender, instance, **kwargs) -> None:
    """Deletes the old image from Cloudinary if it has changed"""
    image_pre_save(sender, instance, field_name='photo_profile')


@receiver(pre_delete, sender=User)
def delete_profile_picture(sender, instance, **kwargs) -> None:
    """Delete the image from Cloudinary before deleting the profile"""
    old_instance = sender.objects.get(pk=instance.pk)
    delete_cloudinary_image(old_instance, field_name='photo_profile')
