from django.urls import path
import apps.jars.views

urlpatterns = [
    path('/jars/tags', apps.jars.views.jars_tag_filter)
]
