from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework import status


class ErrorSerializer(serializers.BaseSerializer):
    def to_representation(self, data):
        return {
            "code": data.get("code"),
            "msg": data.get("msg"),
        }


@api_view(["GET", "POST"])
def page_not_found(request):
    data = {"code": 404, "msg": "page_not_found"}
    serializer = ErrorSerializer(data)
    return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
def page_error(request):
    # data = {"code": 500, "msg": "INTERNAL_SERVER_ERROR"}
    # serializer = ErrorSerializer(data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
