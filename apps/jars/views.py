from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .filters import JarFilter
from .models import Jar
from .permissions import JarPermission
from .serializers import JarsSerializer, JarCreateSerializer


class JarListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating Jars.

    * Requires authentication.
    * Allows GET requests for listing.
    * Allows POST requests for creating (requires active volunteer).

    Query Parameters:
        - `search`: Search by title.
        - `ordering`: Order by date_added.
        - `tags__name`: Filter by tags name.
        - `fill_percentage`: Filter jars by fill percentage.

    Example:
    ```
    /api/jars/?search=example&ordering=-date_added&tags__name=name
    ```

    POST Request Body (for creating a new Jar):
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
        "tags": ["tag1", "tag2"],
        "fill_percentage": "-fill_percentage"
    }
    ```

    Response Example (for successful creation):
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
    }
    ```
    """
    permission_classes = [JarPermission]
    queryset = Jar.objects.all()
    serializer_class = JarsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = JarFilter
    search_fields = ['title']
    ordering_fields = ['date_added']
    filterset_fields = ['tags__name']

    def get_serializer_class(self):
        """
        Get the appropriate serializer class based on the request method.
        Use JarCreateSerializer for POST requests and JarsSerializer for others.
        """
        if self.request.method == 'POST':
            return JarCreateSerializer
        return self.serializer_class
