import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adminx.forms import MangaUploadForm
from api.helpers.serializer import ComicsSuccessSerializer
from adminx.helpers import p_b


@api_view(["GET"])
def check_progress(request):
    key = request.GET.get("key", "")
    if key:
        re = p_b.read(key)
        if isinstance(re, bytes):
            content = eval(re)
            serializer = ComicsSuccessSerializer(content)
            return Response(serializer.data)
    content = [0, "无效key"]
    serializer = ComicsSuccessSerializer(content)
    return Response(serializer.data)


