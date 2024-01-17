from apps.jars.models import JarAlbum, JarTag
from django.core.exceptions import ObjectDoesNotExist

from apps.user.models import VolunteerInfo


def add_tag_to_jar(jar, tags_data) -> None:
    """
    Adds tags to a Jar instance.

    Parameters:
    - jar: The Jar instance.
    - tags_data (list): List of tag names.

    Returns:
    - None
    """
    for tag_data in tags_data:
        try:
            tag = JarTag.objects.get(name=tag_data)
        except ObjectDoesNotExist:
            pass
        else:
            jar.tags.add(tag)


def create_album_for_jar(jar, album) -> None:
    """
    Creates album images for a Jar instance.

    Parameters:
    - jar: The Jar instance.
    - album (list): List of dictionaries containing album image data.

    Returns:
    - None
    """
    for image in album:
        img = image['img']
        img_alt = image['img_alt']
        img_album = JarAlbum.objects.create(jar=jar, img_alt=img_alt)
        img_album.img = img
        img_album.save()


def formate_validate_data(validated_data, request) -> list:
    """
    Formats and validates data for creating a new Jar instance.

    Parameters:
    - validated_data (dict): Validated data for creating the Jar instance.
    - request: The request object.

    Returns:
    - list: List containing formatted data for creating the Jar instance.
    """
    try:
        tags_data = validated_data.pop('tags')
    except KeyError:
        tags_data = []
    try:
        album_data = validated_data.pop('album')
    except KeyError:
        album_data = []
    try:
        validated_data.pop('title_img')
        title_img_data = request.FILES['title_img']
    except KeyError:
        title_img_data = None

    volunteer = VolunteerInfo.objects.get(user=request.user)
    validated_data['volunteer'] = volunteer

    return [validated_data, tags_data, album_data, title_img_data]


def get_album_img_and_img_alt_in_list(files, album_data) -> list:
    """
    Retrieves album images and their alternative texts from form data.

    Parameters:
    - files: Files data from the request.
    - album_data (list): List of dictionaries containing album image data.

    Returns:
    - list: List containing dictionaries with album image data.
    """
    album = []
    for key in files:
        if 'album' in key:
            try:
                img_alt = album_data[int(key[6])]['[img_alt]']
            except KeyError:
                img_alt = None
            album.append({'img': files[key], 'img_alt': img_alt})
    return album
