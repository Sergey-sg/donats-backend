from django.core.exceptions import ObjectDoesNotExist

from shared.cloudinary.utils import get_full_image_url


class JarCurrentSumMixin:
    """
    Mixin to include current sum in Jar serializers.
    """

    def get_current_sum(self, instance) -> int | None:
        """
        Custom method to get the latest current sum in the jar.

        Returns the latest current sum or 0 if no sums are available.

        Args:
        - instance: The Jar instance for which to retrieve the latest current sum.

        Returns:
        - int: The latest current sum or 0 if no sums are available.
        """
        try:
            latest_sum = instance.amountofjar_set.latest('date_added')
            return latest_sum.sum
        except ObjectDoesNotExist:
            return 0


class JarFullTitleUrl:
    """
    Mixin to include full title image URL in Jar serializers.
    """

    def get_title_img(self, obj):
        """
        Returns the full title image URL for the given Jar instance.

        Parameters:
        - obj: The Jar instance.

        Returns:
        - str | None: The full title image URL or None if the image is not available.
        """
        return get_full_image_url(obj, 'title_img')
