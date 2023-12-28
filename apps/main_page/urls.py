from django.urls import path
import apps.main_page.views

urlpatterns = [
    path('/<slug:tag_slug>', apps.main_page.views.main_page)
]
