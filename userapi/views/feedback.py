import os

from PIL import Image
from django.shortcuts import reverse, redirect
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import FeedBackDetailSerializer, ComicsSuccessSerializer, FeedBackAwardSerializer
from userapi.models import FeedBack, FeedBackDetail


class FeedBackDetailClientViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    serializer_class = FeedBackDetailSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'feedback/client.html'

    def retrieve(self, request, *args, **kwargs):
        form = self.serializer_class({"email": request.GET.get("email"),
                                      "title": "", "content": "", "system": ""},
                                     )
        return Response({"serializer": form})

    def update(self, request, *args, **kwargs):
        form = self.serializer_class(data=request.data)
        if form.is_valid():
            title = form.validated_data.get("title")
            email = form.validated_data.get("email")
            system = form.validated_data.get("system")
            content = form.validated_data.get("content")
            pictures = request.FILES.getlist('picture')
            # 生成目录
            target_path = os.path.join(settings.MEDIA_ROOT, "uploads/feedback/%s_%s_%s" %
                                       (email, title, timezone.now().date().strftime("%Y-%m-%d").replace("-", '')))
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
            p_path = "%s_%s_%s" % (email, title, timezone.now().date().strftime("%Y-%m-%d").replace("-", ''))
            fbd = FeedBackDetail(title=title, email=email, system=system,
                                 content=content, picture=p_path)
            fbd.save()
            FeedBack(email=email, fbd_id=fbd.id).save()
            r = reverse("userapi:fbdr")
            return redirect(r)
        else:
            return Response({"serializer": form})


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
