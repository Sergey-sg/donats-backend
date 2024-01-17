from django.urls import path

from .views import UserRetrieveUpdateDestroyView


urlpatterns = [
    path('', UserRetrieveUpdateDestroyView.as_view(), name='user_detail'),
]
