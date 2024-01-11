from django.urls import path

from . import views


urlpatterns = [
    path('', views.JarListCreateView.as_view(), name='jars_list'),
    path('<int:pk>/', views.JarRetrieveUpdateDestroyView.as_view(), name='jar_detail'),
    path('banner/', views.JarsListForBannerView.as_view(), name='banner'),
    path('tags/', views.TagsListView.as_view(), name='tags_list'),
]
