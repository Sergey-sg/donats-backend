from cloudinary import uploader as cloudinary_uploader


def delete_cloudinary_image(old_instance, field_name) -> None:
    """
    Deletes an image from Cloudinary.

    Parameters:
    - old_instance: The old instance of the object.
    - field_name (str): The name of the image field.

    Returns:
    - None
    """
    old_image = getattr(old_instance, field_name, None)
    if old_image and old_image.public_id:
        cloudinary_uploader.destroy(old_image.public_id)


def image_pre_save(sender, instance, field_name) -> None:
    """
    Handles actions before saving an object with an image.

    Parameters:
    - sender: The model class.
    - instance: The instance of the object being saved.
    - field_name (str): The name of the image field.

    Returns:
    - None
    """
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


def get_full_image_url(obj, field_name) -> (str | None):
    """
    Retrieves the full image URL from the given object and field name.

    Parameters:
    - obj: The object containing the image field.
    - field_name (str): The name of the image field.

    Returns:
    - str | None: The full image URL or None if the image is not available.
    """
    image = getattr(obj, field_name, None)
    if image:
        return image.url
    return None
