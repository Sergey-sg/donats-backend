from rest_framework import generics, views, status

from rest_framework.response import Response

from apps.jars import serializers
from apps.jars.models import Jar
from apps.jars.serializers import JarSerializer


class AllJarsView(generics.ListAPIView):
    queryset = Jar.objects.all()
    serializer_class = serializers.JarSerializer


class JarByTagView(views.APIView):
    """
    View to retrieve a list of jars filtered by tag.
    """

    def get(self, request):
        tag = request.GET.get('tag__name')
        if tag:
            jars_with_tag = Jar.objects.filter(tags__name=tag)
            serializer = JarSerializer(jars_with_tag, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("redirect: 'jars/'")

