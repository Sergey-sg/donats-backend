from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import UserRegisterView, UserLoginView, TokenRefreshView


urlpatterns = [
    # /api/auth/...
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
