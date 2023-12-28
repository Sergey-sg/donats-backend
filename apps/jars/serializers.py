from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from rest_framework import serializers

from .models import Jar, JarTag
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


class JarsSerializer(serializers.ModelSerializer):
    """
    Serializer for Jar model.

    Fields:
        - `monobank_id`: Monobank ID of the jar.
        - `title`: Title of the jar.
        - `tags`: List of tags associated with the jar (serialized using JarTagSerializer).
        - `goal`: Goal sum of the jar.
        - `current`: Current sum in the jar.
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
        "goal": 1000,
        "current": 500,
        "date_added": "2023-01-01T12:00:00Z"
    }
    ```
    """
    tags = JarTagSerializer(many=True, read_only=True)

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags', 'goal', 'current', 'date_added']


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
        "tags": [{"name": "savings"}, {"name": "finance"}]
    }
    ```
    """
    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags']

    def create(self, validated_data) -> HttpResponseForbidden | Jar:
        tags_data = validated_data.pop('tags')
        # user = self.context['request'].user
        # try:
        #     volunteer = VolunteerInfo.objects.get(user=user)
        # except ObjectDoesNotExist:
        #     return HttpResponseForbidden("You don't have permission to access this resource.")
        # validated_data['volunteer'] = volunteer
        jar = Jar.objects.create(**validated_data)

        for tag_data in tags_data:
            tag = JarTag.objects.get(name=tag_data['name'])
            jar.tags.add(tag.pk)

        jar.save()

        return jar
