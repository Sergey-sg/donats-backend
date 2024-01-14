from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import User


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting the authenticated user.

    * Requires authentication.
    * Allows GET, PUT, and DELETE requests.

    Example:
    ```
    /api/user/
    ```

    Response Example:
    ```json
    {
        "id": 1,
        "email": "example@example.com",
        // Additional user fields
    }
    ```
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self) -> User:
        """Return authorized user object"""
        return self.request.user