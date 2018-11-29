import os

from PIL import Image
from django.shortcuts import reverse, redirect
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from api.helpers import EnumBase, MyViewBackend, set_attr
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import FeedBackDetailSerializer, ComicsSuccessSerializer, FeedBackAwardSerializer
from userapi.models import FeedBack, FeedBackDetail


class FeedBackDetailClientViewSet(viewsets.ViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            data = self.feed_back_client()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def feed_back_client(self):
        # form = self.serializer_class(data=request.data)
        # if form.is_valid():
        title = getattr(self, "title") if hasattr(self, "title") else None
        email = getattr(self, "email") if hasattr(self, "email") else None
        system = getattr(self, "system") if hasattr(self, "system") else None
        content = getattr(self, "content") if hasattr(self, "content") else None
        pictures = getattr(self, "pictures") if hasattr(self, "pictures") else None
        p_path = "%s_%s_%s" % (email, title, timezone.now().strftime("%Y%m%d%H%M%S"))

        # 生成目录
        target_path = os.path.join(settings.MEDIA_ROOT, "uploads/feedback/%s" % p_path)
        if not os.path.exists(target_path):
            os.mkdir(target_path)
        # 处理图片
        if pictures:
            for k, v in enumerate(pictures):
                p_name = v.name
                img = Image.open(v)
                img.thumbnail((300, 300))
                suffix = os.path.splitext(p_name)[1]
                filename = "%s_%s_%d" % (email, title, k) + suffix
                pathname = os.path.join(target_path, filename)
                img.save(pathname)
        fbd = FeedBackDetail(title=title, system=system,
                             content=content, picture=p_path)
        fbd.save()
        FeedBack(email=email, fbd_id=fbd.id).save()
        # r = reverse("userapi:fbdr")
        data = ComicMethod.pack_success_data()

        return data


@api_view(["GET"])
def feedback_detail_return(request):
    data = ComicMethod.pack_success_data()
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["POST", "GET"])
@renderer_classes([TemplateHTMLRenderer])
def feedback_award(request, *args, **kwargs):
    form_p = FeedBackAwardSerializer(data=request.data)
    fbd_id = kwargs.get("fbd_id")
    redirect_to = request.GET.get('next', '')
    form = FeedBackAwardSerializer({"id": fbd_id, "award": None})
    if fbd_id:
        fbd = FeedBackDetail.get(id=fbd_id)
        picture_path = os.path.join(settings.MEDIA_ROOT, "uploads/feedback", str(fbd.picture))
        pl = []
        for p in os.listdir(picture_path):
            pl.append(os.path.join("img/uploads/feedback", str(fbd.picture), p))
        fbd.picture = pl
        fb = FeedBack.get(fbd_id=fbd_id)
        fbd.award = fb.award
        fbd.status = fb.status
        if request.method == "GET":
            return Response({"context": fbd, "next": redirect_to, "serializer": form},
                            template_name='feedback/server.html')
        else:
            if form_p.is_valid():
                award = form_p.validated_data.get("award")
                fb.award = award
                fb.status = 1
                fb.save()
                return redirect(redirect_to)
            return Response({"context": fbd, "next": redirect_to, "serializer": form_p},
                            template_name='feedback/server.html')
