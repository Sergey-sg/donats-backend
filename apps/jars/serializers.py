from rest_framework import serializers
from django.db import transaction

from shared.cloudinary.utils import get_full_image_url

from .mixins import JarCurrentSumMixin, JarFullTitleUrl
from .models import Jar, JarAlbum, JarTag, AmountOfJar
from .utils import add_tag_to_jar, create_album_for_jar, formate_validate_data, get_album_img_and_img_alt_in_list


class JarTagSerializer(serializers.ModelSerializer):
    """
    Serializer for JarTag model.

    Fields:
        - `id` (int): The unique identifier for the tag.
        - `name`: The name of the tag.

    Example:
    ```json
    {
        "id": 1,
        "name": "category1"
    }
    ```
    """
    class Meta:
        model = JarTag
        fields = ['id', 'name']


class AmountOfJarSerializer(serializers.ModelSerializer):
    """
    Serializer for the current sum of a Jar model.

    Fields:
        - `id` (int): The unique identifier for the AmountOfJar.
        - `sum` (int): The current sum in the jar.
        - `date_added` (datetime): Date when the amount was added.
        - `incomes` (int): the income difference.

    Example:
    ```json
    {
        "id": 1,
        "sum": 100000,
        "incomes": 20000,
        "date_added": "2023-01-01T12:00:00Z"
    }
    ```
    """
    class Meta:
        model = AmountOfJar
        fields = ['id', 'sum', 'incomes', 'date_added']


class JarsSerializer(serializers.ModelSerializer, JarCurrentSumMixin, JarFullTitleUrl):
    """
    Serializer for the Jar model.

    Fields:
    - `id` (int): The unique identifier for the jar.
    - `monobank_id` (str): Monobank ID of the jar.
    - `title` (str): Title of the jar.
    - `description` (str): Description for jar.
    - `tags` (List[JarTagSerializer]): List of tags associated with the jar.
    - `volunteer` (str): Public name of the volunteer associated with the jar.
    - `title_img`: A method field returning the title image of the jar.
    - `img_alt` (str): The alternative text for the jar image.
    - `goal` (float): Goal sum of the jar.
    - `current_sum`: A method field returning the current sum of the jar.
    - `date_added` (datetime): Date when the jar was added.
    - `date_closed` (datetime): Date when the jar was closed.

    Example:
    ```json
    {
        "id": 1,
        "monobank_id": "12345678901",
        "title": "Savings Jar",
        "description": "Description for jar",
        "tags": [
            {"id": 1, "name": "category1"},
            {"id": 2, "name": "category2"}
        ],
        "volunteer": "JohnDoe",
        "title_img": "https://example.com/savings-jar.jpg",
        "img_alt": "Savings Jar Image",
        "goal": 1000,
        "current_sum": 500,
        "date_added": "2023-01-01T12:00:00Z",
        "date_closed": "2023-02-01T12:00:00Z"
    }
    ```
    """
    tags = JarTagSerializer(many=True, read_only=True)
    current_sum = serializers.SerializerMethodField()
    volunteer = serializers.CharField(
        source='volunteer.public_name', read_only=True)
    title_img = serializers.SerializerMethodField()

    class Meta:
        model = Jar
        fields = ['id', 'monobank_id', 'title', 'description', 'tags', 'volunteer',
                  'title_img', 'img_alt', 'goal', 'current_sum', 'date_added', "date_closed"]


class JarAlbumSerializer(serializers.ModelSerializer):
    """
    Serializer for the JarAlbum model.

    Fields:
    - `id` (int): The unique identifier for the jar album.
    - `img`: A method field returning the full image URL for the jar album.
    - `img_alt` (str): The alternative text for the jar album image.

    Example:
    ```json
    {
        "id": 1,
        "img": "https://example.com/jar-album.jpg",
        "img_alt": "Jar Album Image"
    }
    ```
    """
    img = serializers.SerializerMethodField()

    class Meta:
        model = JarAlbum
        fields = ['id', 'img', 'img_alt']

    def get_img(self, obj) -> str | None:
        return get_full_image_url(obj, 'img')


class JarCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Jar instance.

    Fields:
    - `monobank_id` (str): Monobank ID of the jar.
    - `title` (str): Title of the jar.
    - `description` (str): Description for jar.
    - `tags` (List): List of tags associated with the jar.
    - `title_img` (File): Title image for the jar.
    - `img_alt` (str): Alternative text for the jar image.
    - `album` (List): List of album images for the jar.

    Example:
    ```json
    {
        "monobank_id": "12345678901",
        "title": "New Savings Jar",
        "description": "Description for jar",
        "tags": ["category1", "category2"],
        "title_img": <file>,
        "img_alt": "New Savings Jar Image",
        "album": [
            {"img": <file>, "img_alt": "Album Image 1"},
            {"img": <file>, "img_alt": "Album Image 2"}
        ]
    }
    ```
    """
    tags = serializers.ListField(write_only=True, required=False)
    album = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'description', 'tags',
                  'title_img', 'img_alt', 'album']

    @transaction.atomic
    def create(self, validated_data) -> Jar:
        """
        Custom method to create a new Jar instance.

        Returns:
            - Jar: The created Jar instance.
        """
        validated_data, tags_data, album_data, title_img_data = formate_validate_data(
            validated_data, self.context['request'])
        jar = Jar.objects.create(**validated_data)
        jar.title_img = title_img_data

        add_tag_to_jar(jar, tags_data)

        album = get_album_img_and_img_alt_in_list(
            self.context['request'].FILES, album_data)

        create_album_for_jar(jar, album)

        jar.save()

        return jar


class JarUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the Jar instance.

    Fields:
    - `title` (str): Title of the jar.
    - `description` (str): Description for jar.
    - `tags` (List): List of tags associated with the jar.
    - `title_img` (File): Title image for the jar.
    - `img_alt` (str): Alternative text for the jar image.
    - `album` (List): List of album images for the jar.

    Example:
    ```json
    {
        "title": "New Savings Jar",
        "description": "Description for jar",
        "tags": ["category1", "category2"],
        "title_img": <file>,
        "img_alt": "New Savings Jar Image",
        "album": [
            {"img": <file>, "img_alt": "Album Image 1"},
            {"img": <file>, "img_alt": "Album Image 2"}
        ]
    }
    ```
    """
    tags = serializers.ListField(write_only=True, required=False)
    album = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Jar
        fields = ['title', 'description', 'tags',
                  'title_img', 'img_alt', 'album']

    @transaction.atomic
    def update(self, instance, validated_data) -> Jar:
        """
        Custom method to update an existing Jar instance.

        Returns:
            - Jar: The updated Jar instance.
        """
        validated_data, tags_data, album_data, title_img_data = formate_validate_data(
            validated_data, self.context['request'])

        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.img_alt = validated_data['img_alt']
        instance.title_img = title_img_data

        instance.tags.clear()
        add_tag_to_jar(instance, tags_data)

        album = get_album_img_and_img_alt_in_list(
            self.context['request'].FILES, album_data)

        create_album_for_jar(instance, album)

        instance.save()

        return instance


class JarSerializer(serializers.ModelSerializer, JarCurrentSumMixin, JarFullTitleUrl):
    """
    Serializer for the detailed representation of a Jar.

    Fields:
    - `id` (int): The unique identifier for the jar.
    - `monobank_id` (str): Monobank ID of the jar.
    - `title` (str): Title of the jar.
    - `description` (str): Description for jar.
    - `tags` (List[JarTagSerializer]): List of tags associated with the jar.
    - `volunteer` (str): Public name of the volunteer associated with the jar.
    - `title_img`: A method field returning the title image of the jar.
    - `img_alt` (str): The alternative text for the jar image.
    - `album` (List[JarAlbumSerializer]): List of album images associated with the jar.
    - `goal` (float): Goal sum of the jar.
    - `current_sum`: A method field returning the current sum of the jar.
    - `date_added` (datetime): Date when the jar was added.

    Example:
    ```json
    {
        "id": 1,
        "monobank_id": "12345678901",
        "title": "Savings Jar",
        "description": "Description for jar",
        "tags": [
            {"id": 1, "name": "category1"},
            {"id": 2, "name": "category2"}
        ],
        "volunteer": "JohnDoe",
        "title_img": "https://example.com/savings-jar.jpg",
        "img_alt": "Savings Jar Image",
        "album": [
            {"id": 1, "img": "https://example.com/jar-album-1.jpg", "img_alt": "Album Image 1"},
            {"id": 2, "img": "https://example.com/jar-album-2.jpg", "img_alt": "Album Image 2"}
        ],
        "goal": 1000,
        "current_sum": 500,
        "date_added": "2023-01-01T12:00:00Z"
    }
    """
    tags = JarTagSerializer(many=True, read_only=True)
    current_sum = serializers.SerializerMethodField()
    volunteer = serializers.CharField(
        source='volunteer.public_name', read_only=True)
    title_img = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()

    class Meta:
        model = Jar
        fields = ['id', 'monobank_id', 'title', 'description', 'tags', 'volunteer',
                  'title_img', 'img_alt', 'album', 'goal', 'current_sum', 'date_added']

    def get_album(self, obj) -> list:
        """
        Returns the list of album images associated with the jar.

        Returns:
        - List[dict]: List of serialized JarAlbum instances.
        """
        album = []
        for image in obj.jaralbum_set.all():
            album.append(JarAlbumSerializer(image).data)
        return album
