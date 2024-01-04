from cloudinary import uploader as cloudinary_uploader


def delete_cloudinary_image(old_instance, field_name) -> None:
    """A function to delete an image from Cloudinary"""
    old_image = getattr(old_instance, field_name, None)
    if old_image.public_id:
        cloudinary_uploader.destroy(old_image.public_id)


def image_pre_save(sender, instance, field_name, **kwargs):
    """Handles actions before saving an object with an image."""
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        old_image = getattr(old_instance, field_name, None)
        new_image = getattr(instance, field_name, None)
        if old_image and old_image != new_image:
            delete_cloudinary_image(old_instance, field_name)

        if not new_image:
            instance.img_alt = None

    except sender.DoesNotExist:
        pass
