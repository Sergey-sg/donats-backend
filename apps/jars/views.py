import json

from django.core.serializers import serialize
from django.urls import reverse

from apps.jars.models import Jar, JarTag
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseServerError
)


def all_jars(request):
    try:
        jars = Jar.objects.all()
        jars_serialized = serialize('json', jars)
        jars_json = json.loads(jars_serialized)
        return JsonResponse(jars_json, safe=False)
    except:
        return HttpResponseServerError()


def jars_tag_filter(request):
    filter_tag = request.GET.get('filter_tag', None)

    if filter_tag:
        try:
            tag = JarTag.objects.get(name=filter_tag)
            filtered_jars_query = Jar.objects.filter(tags=tag)
            filtered_jars_serialized = serialize('json', filtered_jars_query)
            filtered_jars_json = json.loads(filtered_jars_serialized)
            return JsonResponse(filtered_jars_json, safe=False)
        except JarTag.DoesNotExist:
            return HttpResponseBadRequest("Tag doesn't exist")
    else:
        return HttpResponseRedirect(reverse('jars_list'))
