from rest_framework import serializers

from .models import Jar, JarTag, JarCurrentSum


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


class JarSerializer(serializers.ModelSerializer):
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
        fields = ['monobank_id', 'title', 'volunteer', 'tags', 'goal', 'date_added']


class JarCurrentSumSerializer(serializers.ModelSerializer):
    """
    Serializer for JarCurrentSum model.

    Fields:
        - `sum` (int): The sum in the jar.
        - `jar` (bigint): The reference to the jar.
        - `date_added` (date): Date when sum info was added.

    Example:
    ```json
    {
        "sum": "10000",
        "jar":
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
        "date_added": "2023-01-01"
    }
    ```
    """
    jar = JarSerializer(many=False, read_only=True)

    class Meta:
        model = JarCurrentSum
        fields = ['sum', 'jar', 'date_added']


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

    def create(self, validated_data) -> Jar:
        tags_data = validated_data.pop('tags')
        jar = Jar.objects.create(**validated_data)

        for tag_data in tags_data:
            tag = JarTag.objects.get(name=tag_data['name'])
            jar.tags.add(tag)

        jar.save()

        return jar
