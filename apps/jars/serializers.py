from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from rest_framework import serializers
from django.db import transaction

from shared.cloudinary.utils import get_full_image_url

from .mixins import JarCurrentSumMixin, JarFullTitleUrl
from .models import Jar, JarAlbum, JarTag, AmountOfJar
from ..user.models import VolunteerInfo


class JarTagSerializer(serializers.ModelSerializer):
    """
    Serializer for JarTag model.

    Fields:
        - `name`: The name of the tag.

    Example:
    ```json
    {
        "name": "category1"
    }
    ```
    """
    class Meta:
        model = JarTag
        fields = ['name']


class JarCurrentSumSerializer(serializers.ModelSerializer):
    """
    Serializer for the current sum of a Jar model.

    Fields:
        - `sum` (int): The current sum in the jar.

    Example:
    ```json
    {
        "sum": 500
    }
    ```
    """
    class Meta:
        model = AmountOfJar
        fields = ['sum']


class JarsSerializer(serializers.ModelSerializer, JarCurrentSumMixin, JarFullTitleUrl):
    """
    Serializer for Jar model.

    Fields:
        - `monobank_id`: Monobank ID of the jar.
        - `title`: Title of the jar.
        - `tags`: List of tags associated with the jar (serialized using JarTagSerializer).
        - `volunteer`: Public name of the volunteer associated with the jar.
        - `goal`: Goal sum of the jar.
        - `current_sum`: Current sum in the jar.
        - `date_added`: Date when the jar was added.

    Example:
    ```json
    {
        "monobank_id": "12345678901",
        "title": "Savings Jar",
        "tags": [
            {"name": "category1"},
            {"name": "category2"}
        ],
        "volunteer": "JohnDoe",
        "goal": 1000,
        "current_sum": 500,
        "date_added": "2023-01-01T12:00:00Z"
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
        fields = ['id', 'monobank_id', 'title', 'tags', 'volunteer',
                  'title_img', 'img_alt', 'goal', 'current_sum', 'date_added']


class JarAlbumSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = JarAlbum
        fields = ['img', 'img_alt']

    def get_img(self, obj) -> str | None:
        return get_full_image_url(obj, 'img')

class JarCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Jar instance.

    Fields:
        - `monobank_id` (str): The ID of the jar in Monobank.
        - `title` (str): The title of the jar.
        - `tags` (list): List of tags associated with the jar.

    Example:
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
        "tags": ["cars", "drons"]
    }
    ```
    """
    tags = serializers.ListField(write_only=True, required=False)
    album = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags', 'title_img', 'img_alt', 'album']

    @transaction.atomic
    def create(self, validated_data) -> HttpResponseForbidden | Jar:
        """
        Custom method to create a new Jar instance.

        Returns the created Jar instance or HttpResponseForbidden if the user does not have permission.
        """
        try:
            tags_data = validated_data.pop('tags')
        except KeyError:
            tags_data = []
        try:
            validated_data.pop('album')
        except KeyError:
            pass
        try:
            validated_data.pop('title_img')
            title_img_data = self.context['request'].FILES['title_img']
        except KeyError:
            title_img_data = None
        try:
            print(validated_data)
            album_img_alt = validated_data.pop('album_img_alt')
        except KeyError:
            album_img_alt = []

        volunteer = VolunteerInfo.objects.get(user=self.context['request'].user)
        validated_data['volunteer'] = volunteer

        jar = Jar.objects.create(**validated_data)
        jar.title_img = title_img_data

        for tag_data in tags_data:
            try:
                tag = JarTag.objects.get(name=tag_data)
            except ObjectDoesNotExist:
                pass
            else:
                jar.tags.add(tag)

        album_files = self.context['request'].FILES.getlist('album', []) 
        print(len(album_files))
        for index in range(len(album_files)):
            img = album_files[index]
            try:
                img_alt = album_img_alt[index]
            except IndexError:
                img_alt = None
            print(f'\n{index} {img_alt}\n')
            img_album = JarAlbum.objects.create(jar=jar, img_alt=img_alt)
            img_album.img = img
            img_album.save()

        jar.save()

        return jar


class JarsForBannerSerializer(serializers.ModelSerializer, JarCurrentSumMixin, JarFullTitleUrl):
    """
    Serializer for interacting with a list of banners for jars.

    Fields:
    - id: Unique identifier for the jar.
    - title: Title of the jar.
    - tags: List of tags associated with the jar.
    - goal: Target amount to achieve.
    - current_sum: Current amount of funds in the jar.
    - date_added: Date when the jar was added.

    Example:
    ```json
    {
        "id": 1,
        "title": "Savings Jar",
        "tags": [
            {"name": "category1"},
            {"name": "category2"}
        ],
        "goal": 1000,
        "current_sum": 500,
        "date_added": "2023-01-01T12:00:00Z"
    }
    ```
    """
    tags = JarTagSerializer(many=True, read_only=True)
    current_sum = serializers.SerializerMethodField()
    title_img = serializers.SerializerMethodField()

    class Meta:
        model = Jar
        fields = ['id', 'title', 'tags', 'title_img',
                  'img_alt', 'goal', 'current_sum', 'date_added']


class JarSerializer(serializers.ModelSerializer, JarCurrentSumMixin, JarFullTitleUrl):
    tags = JarTagSerializer(many=True, read_only=True)
    current_sum = serializers.SerializerMethodField()
    volunteer = serializers.CharField(
        source='volunteer.public_name', read_only=True)
    title_img = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()

    class Meta:
        model = Jar
        fields = ['id', 'monobank_id', 'title', 'tags', 'volunteer',
                  'title_img', 'img_alt', 'album', 'goal', 'current_sum', 'date_added']    
        
    def get_album(self, obj):
        album = []
        for image in obj.jaralbum_set.all():
            album.append(JarAlbumSerializer(image).data)
        return album
