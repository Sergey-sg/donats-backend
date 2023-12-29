from django.urls import path

from . import views


urlpatterns = [
    path('', views.JarsListView.as_view(), name='jars_list'),
    path('create/', views.JarCreateView.as_view(), name='jar_create'),
]
