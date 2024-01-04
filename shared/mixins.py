from django.core.exceptions import ObjectDoesNotExist


class JarCurrentSumMixin:
    def get_current_sum(self, instance) -> int | None:
        """
        Custom method to get the latest current sum in the jar.

        Returns the latest current sum or None if no sums are available.

        Args:
        - instance: The Jar instance for which to retrieve the latest current sum.

        Returns:
        - int | None: The latest current sum or None if no sums are available.
        """
        try:
            latest_sum = instance.jarcurrentsum_set.latest('date_added')
            from apps.jars.serializers import JarCurrentSumSerializer
            return JarCurrentSumSerializer(latest_sum).data["sum"]
        except ObjectDoesNotExist:
            return None
