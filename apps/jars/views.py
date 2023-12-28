import json.encoder

from apps.jars.models import Jar, JarTag
from django.http import HttpResponseBadRequest


def jars_tag_filter(request):
    filter_tag = request.GET['filter_tag']

    try:
        tag = JarTag.objects.get(name=filter_tag)
        jars = Jar.objects.filter(tags=tag)
        return json.encoder.JSONEncoder().encode(jars)
    except JarTag.DoesNotExist:
        return HttpResponseBadRequest("Tag doesn't exist")
