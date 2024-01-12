from django.db import models


class AmountOfJarManager(models.Manager):
    """
    Custom manager for the AmountOfJar model.

    Provides additional methods for creating and managing AmountOfJar instances.
    """

    def create_and_calculate_difference(self, jar, sum):
        """
        Create a new AmountOfJar instance and calculate the income difference.

        Parameters:
            - jar (Jar): The Jar for which the AmountOfJar instance is created.
            - sum (int): The current sum to be set for the new AmountOfJar instance.

        Returns:
            AmountOfJar: The newly created AmountOfJar instance with the calculated income difference.

        Example:
            new_amount = AmountOfJar.objects.create_and_calculate_difference(my_jar_instance, new_sum_value)
        """
        latest_sum = self.filter(jar=jar).latest('date_added')
        incomes = sum - (latest_sum.sum if latest_sum else 0)
        new_amount = self.create(jar=jar, sum=sum, incomes=incomes)

        return new_amount
