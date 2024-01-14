from rest_framework import serializers
from apps.user.models import User
from shared.cloudinary.utils import get_full_image_url


class UserSerializer(serializers.ModelSerializer):
    photo_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'photo_profile']

    def get_photo_profile(self, obj):
        """
        Returns the full photo profile image URL for the given User instance.

        Parameters:
        - obj: The User instance.

        Returns:
        - str | None: The full photo profile image URL or None if the image is not available.
        """
        return get_full_image_url(obj, 'photo_profile')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email',]
