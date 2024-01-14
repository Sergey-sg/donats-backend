from django.urls import path, include

from .views import UserRetrieveUpdateDestroyView


urlpatterns = [
    path('', UserRetrieveUpdateDestroyView, name='user_detail'),
]
