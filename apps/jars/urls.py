from django.urls import path
import apps.jars.views

urlpatterns = [
    # path('', views.all_jars, name='jars_list'),
    path('', views.JarsListView.as_view(), name='jars_list'),
    path('tags/', views.jars_tag_filter),
    path('create/', views.JarCreateView.as_view(), name='jar_create')
    path('', views.AllJarsView.as_view(), name='all-jars-view'),
    path('tags/', views.JarByTagView.as_view(), name='jars-tag-filter-view')
]
