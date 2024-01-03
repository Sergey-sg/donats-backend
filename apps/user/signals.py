from cloudinary import uploader as cloudinary_uploader
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import User


def delete_cloudinary_image(public_id) -> None:
    """A function to delete an image from Cloudinary"""
    if public_id:
        cloudinary_uploader.destroy(public_id)


# Signal before saving the User object
@receiver(pre_save, sender=User)
def delete_old_profile_picture(sender, instance, **kwargs) -> None:
    """Deletes the old image from Cloudinary if it has changed"""
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.photo_profile and old_instance.photo_profile != instance.photo_profile:
            delete_cloudinary_image(old_instance.photo_profile.public_id)

        if instance.photo_profile and not instance.photo_alt:
            instance.photo_alt = f"Alt text for {instance.email} photo profile"

        if not instance.photo_profile:
            instance.photo_alt = None
    except sender.DoesNotExist:
        pass


# Signal before deleting the User object
@receiver(pre_delete, sender=User)
def delete_profile_picture(sender, instance, **kwargs):
    """Delete the image from Cloudinary before deleting the profile"""
    delete_cloudinary_image(instance.photo_profile.public_id)
