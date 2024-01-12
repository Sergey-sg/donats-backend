from apps.jars.models import AmountOfJar


new_amount = AmountOfJar.objects.create_and_calculate_difference(86, 1000)