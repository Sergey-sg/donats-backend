from django.urls import path

from . import views


urlpatterns = [
    path('', views.JarListCreateView.as_view(), name='jars_list'),
    path('banner/', views.JarsListForBannerView.as_view(), name='banner')
]
