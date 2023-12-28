from rest_framework import serializers

from .models import Jar, JarTag


class JarTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = JarTag
        fields = ['name']


class JarsSerializer(serializers.ModelSerializer):
    tags = JarTagSerializer(many=True, read_only=True)

    class Meta:
        model = Jar
        fields = ['monobank_id', 'title', 'tags', 'goal', 'current', 'date_added']
