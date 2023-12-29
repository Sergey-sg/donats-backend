import json

from django.core.serializers import serialize
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseServerError
)

from .models import Jar, JarTag
from .serializers import JarsSerializer, JarCreateSerializer


def all_jars(request):
    try:
        jars = Jar.objects.all()
        jars_serialized = serialize('json', jars)
        jars_json = json.loads(jars_serialized)
        return JsonResponse(jars_json, safe=False)
    except:
        return HttpResponseServerError()


def jars_tag_filter(request):
    filter_tag = request.GET.get('filter_tag', None)

    if filter_tag:
        try:
            tag = JarTag.objects.get(name=filter_tag)
            filtered_jars_query = Jar.objects.filter(tags=tag)
            filtered_jars_serialized = serialize('json', filtered_jars_query)
            filtered_jars_json = json.loads(filtered_jars_serialized)
            return JsonResponse(filtered_jars_json, safe=False)
        except JarTag.DoesNotExist:
            return HttpResponseBadRequest("Tag doesn't exist")
    else:
        return HttpResponseRedirect(reverse('jars_list'))


class JarsListView(generics.ListAPIView):
    """
    View to list Jars.

    * Requires no authentication.
    * Returns a list of Jars.

    Query Parameters:
        - `search`: Search by title.
        - `ordering`: Order by date_added.
        - `tags__name`: Filter by tags name.

    Example:
    ```
    /api/jars/?search=example&ordering=-date_added&tags__name=name
    ```
    """
    permission_classes = [AllowAny]
    queryset = Jar.objects.all()
    serializer_class = JarsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['date_added']
    filterset_fields = ['tags__name']


class JarCreateView(generics.ListCreateAPIView):
    """
    API view for creating a new Jar instance.

    - Requires the user to be authenticated.
    - Supports creating a new Jar instance.

    Request Method:
        - POST: Create a new Jar instance.

    Request Body (for POST request):
        - `monobank_id` (str): The ID of the jar in Monobank (required).
        - `title` (str): The title of the jar (required).
        - `tags` (list): List of tags associated with the jar.

    Example:
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
        "tags": ["cars", "drons"]
    }
    ```

    Response:
    - Status Code: 201 Created (for successful creation).
    - Status Code: 400 Bad Request (for validation errors).

    Response Example (for successful creation):
    ```json
    {
        "monobank_id": "1234567890",
        "title": "Savings Jar",
    }
    ```
    """
    queryset = Jar.objects.none()
    serializer_class = JarCreateSerializer
    # permission_classes = [IsAuthenticated]
