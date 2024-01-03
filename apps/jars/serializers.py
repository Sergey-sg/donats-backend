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
    volunteer = serializers.CharField(source='volunteer.public_name', read_only=True)

    class Meta:
        model = Jar
        fields = ['pk', 'monobank_id', 'title', 'tags', 'volunteer', 'goal', 'current_sum', 'date_added']

    def get_current_sum(self, instance) -> int | None:
        """
        Custom method to get the latest current sum in the jar.

        Returns the latest current sum or None if no sums are available.
        """
        try:
            latest_sum = instance.jarcurrentsum_set.filter().latest('date_added')
            return JarCurrentSumSerializer(latest_sum).data["sum"]
        except ObjectDoesNotExist:
            return None


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
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags']

    def create(self, validated_data) -> HttpResponseForbidden | Jar:
        """
        Custom method to create a new Jar instance.

        Returns the created Jar instance or HttpResponseForbidden if the user does not have permission.
        """
        tags_data = validated_data.pop('tags')
        user = self.context['request'].user
        try:
            volunteer = VolunteerInfo.objects.get(user=user)
        except ObjectDoesNotExist:
            return HttpResponseForbidden("You don't have permission to access this resource.")
        validated_data['volunteer'] = volunteer
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
