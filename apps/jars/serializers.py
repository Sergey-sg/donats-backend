from rest_framework import serializers

from .models import Jar, JarTag


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
