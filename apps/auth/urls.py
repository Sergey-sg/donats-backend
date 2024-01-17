from django.urls import path

from .views import LogoutView, UserRegisterView, UserLoginView, TokenRefreshView


urlpatterns = [
    # /api/auth/...
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
]
