from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from rest_framework import serializers

from .models import Jar, JarTag, JarCurrentSum
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
        model = JarCurrentSum
        fields = ['sum']


class JarsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Jar model.

    Fields:
        - `monobank_id` (str): The ID of the jar in Monobank.
        - `title` (str): The title of the jar.
        - `tags` (list): List of tags associated with the jar (serialized using JarTagSerializer).
        - `goal` (int): Goal sum of the jar.
        - `current_sums` (list): List of current sums in the jar (serialized using JarCurrentSumSerializer).
        - `date_added` (datetime): Date and time when the jar was added.

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
        "current_sums": [{"sum": 500}, {"sum": 600}],
        "date_added": "2023-01-01T12:00:00Z"
    }
    ```
    """
    tags = JarTagSerializer(many=True, read_only=True)
    current_sums = JarCurrentSumSerializer(many=True, read_only=True, source='jarcurrentsum_set')

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags', 'goal', 'current_sums', 'date_added']


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
        "tags": ["tag1", "tag2"]
    }
    ```
    """
    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags']

    tags = serializers.ListField(write_only=True)

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
            try:
                tag = JarTag.objects.get(name=tag_data)
            except ObjectDoesNotExist:
                pass
            else:
                jar.tags.add(tag)

        jar.save()

        return jar
