from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import r1, EnumBase, MyViewBackend, set_attr
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.views import ComicsListBaseView
from userapi.models import Comment


class CommentListViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    list_per_page = 10

    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            data = self.comment_list()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def comment_list(self):
        com_id = getattr(self, "comics_id")
        lang = getattr(self, "lang", "ms")
        page = getattr(self, "current_page", "1")
        comment_list = self.get_queryset(Comment, {"com_id": com_id, "is_delete": 0, "lang": lang},
                                         perm_type="and").order_by("-rate", "-created")
        if not comment_list:
            result_list = []
        else:
            result_list = self.get_comment_list(comment_list)
        obj, current_page, total_page = self.comics_list_paginator(result_list, page)
        return ComicMethod.pack_success_data(comments_list=list(obj), current_page=current_page,
                                             total_page=total_page)

        pass


class CommentUpdateViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.comment_update()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def comment_update(self):
        email = getattr(self, "email")
        lang = getattr(self, "lang", "ms")
        title = getattr(self, "title")
        content = getattr(self, "content")
        com_id = getattr(self, "comics_id")
        rate = getattr(self, "rate")

        try:
            if hasattr(self, "cid"):
                Comment.filter(id=getattr(self, "cid")).update(is_delete=1)
            else:
                c = Comment(email=email, lang=lang, title=title, content=content, com_id=com_id, rate=rate)
                c.save()
        except:
            return EnumBase.get_status(644, CodeEn, lang)  # 发布评论失败
        else:
            return ComicMethod.pack_success_data()
