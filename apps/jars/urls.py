from django.urls import path

from apps.jars import views


urlpatterns = [
    path('', views.AllJarsView.as_view(), name='all-jars-view'),
    path('tags/', views.JarByTagView.as_view(), name='jars-tag-filter-view')
]
