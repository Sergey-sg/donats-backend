from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny

from .filters import JarFilter
from .models import Jar, JarTag
from .permissions import JarPermission
from .serializers import JarSerializer, JarTagSerializer, JarUpdateSerializer, JarsSerializer, JarCreateSerializer


class JarListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating Jars.

    * Allows GET requests for listing.
    * Allows POST requests for creating (requires active volunteer).

    Query Parameters:
        - `search`: Search by title.
        - `ordering`: Order by date_added.
        - `tags`: Filter by tags name.
        - `fill_percentage`: Filter jars by fill percentage.

    Example:
    ```
    /api/jars/?search=example&ordering=-date_added&tags=name&fill_percentage=-fill_percentage
    ```

    POST Request Body (for creating a new Jar):
    ```json
    {
        "monobank_id": "12345678901",
        "title": "New Savings Jar",
        "tags": ["category1", "category2"],
        "title_img": <file>,
        "img_alt": "New Savings Jar Image",
        "album": [
            {"img": <file>, "img_alt": "Album Image 1"},
            {"img": <file>, "img_alt": "Album Image 2"}
        ]
    }
    ```

    Response Example (for successful creation):
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
        "title_img": "https://example.com/jar-album.jpg",
        "img_alt": "New Savings Jar Image",
    }
    ```
    """
    permission_classes = [JarPermission]
    queryset = Jar.objects.all()
    serializer_class = JarsSerializer
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = JarFilter
    search_fields = ['title']
    ordering_fields = ['date_added']
    # filterset_fields = ['tags__name']

    def get_serializer_class(self) -> Type[JarCreateSerializer | JarsSerializer]:
        """
        Get the appropriate serializer class based on the request method.
        Use JarCreateSerializer for POST requests and JarsSerializer for others.
        """
        if self.request.method == 'POST':
            return JarCreateSerializer
        return self.serializer_class


class JarsListForBannerView(generics.ListAPIView):
    """
    API view for listing Jars for banner display.

    * Allows GET requests for listing.

    Example:
    ```
    /api/jars/banner/
    ```

    Response Example:
    ```json
    [
        {
            "id": 1,
            "monobank_id": "12345678901",
            "title": "Savings Jar",
            "tags": [
                {"id": 1, "name": "category1"},
                {"id": 2, "name": "category2"}
            ],
            "volunteer": "JohnDoe",
            "title_img": "https://example.com/savings-jar.jpg",
            "img_alt": "Savings Jar Image",
            "goal": 1000,
            "current_sum": 500,
            "date_added": "2023-01-01T12:00:00Z"
        },
        // Additional Jar items
    ]
    ```
    """
    serializer_class = JarsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet:
        """
        Get the first 8 Jars ordered by 'dd_order'.
        """
        try:
            jars = Jar.objects.filter(date_closed=None).order_by('dd_order')[:8]
        except ObjectDoesNotExist:
            jars = Jar.objects.none()
        return jars


class JarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific Jar.

    * Allows GET requests for retrieving.
    * Allows PUT requests for updating (requires active volunteer).
    * Allows DELETE requests for deleting (requires active volunteer).

    Example:
    ```
    /api/jars/1/
    ```

    PUT Request Body (for updating an existing Jar):
    ```json
    {
        "title": "Updated Savings Jar",
        "tags": ["category1", "category2"],
        "title_img": <file>,
        "img_alt": "Updated Savings Jar Image",
        "album": [
            {"img": <file>, "img_alt": "Updated Album Image 1"},
            {"img": <file>, "img_alt": "Updated Album Image 2"}
        ]
    }
    ```

    Response Example (for successful update):
    ```json
    {
        "title": "Updated Savings Jar",
        "title_img": "<url>",
        "img_alt": "Updated Savings Jar Image",
    }
    ```

    DELETE Request:
    ```
    /api/jars/1/
    ```
    Response Example (for successful delete):
    ```json
    {
        "detail": "Jar successfully deleted."
    }
    ```
    """
    permission_classes = [JarPermission]
    queryset = Jar.objects.all()
    serializer_class = JarSerializer

    def get_serializer_class(self) -> Type[JarUpdateSerializer | JarSerializer]:
        """
        Get the appropriate serializer class based on the request method.
        Use JarUpdateSerializer for PUT requests and JarSerializer for others.
        """
        if self.request.method == 'PUT':
            return JarUpdateSerializer
        return self.serializer_class


class TagsListView(generics.ListAPIView):
    """
    API view for listing Tags for jars display.

    * Allows GET requests for listing.

    Example:
    ```
    /api/jars/tags/
    ```

    Response Example:
    ```json
    [
        {
        "id": 1,
        "name": "category1"
        },
        // Additional Tags items
    ]
    ```
    """
    permission_classes = [AllowAny]
    queryset = JarTag.objects.all()
    serializer_class = JarTagSerializer
