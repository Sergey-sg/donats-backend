from django.urls import path
import apps.jars.views

urlpatterns = [
    path('', apps.jars.views.all_jars, name='jars_list'),
    path('tags/', apps.jars.views.jars_tag_filter)
]
