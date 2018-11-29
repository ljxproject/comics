from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import r, MyViewBackend, set_attr
from api.helpers.myenum import EnumBase
from api.helpers.code import CodeEn, CategoryEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.models import Search, ComicInfo
from userapi.models import PurchaseAndFavorite
from api.views import ComicsListBaseView


class ComicsListViewSet(viewsets.ViewSet, ComicsListBaseView, MyViewBackend):

    def get_model(self):
        pass

    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            lang = getattr(self, "lang", "ms")
            page = getattr(self, "current_page", "1")
            data = self.category_comics_handler(lang, page)
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def category_comics_handler(self, lang, page):
        if not hasattr(self, "category"):
            return EnumBase.get_status(622, CodeEn, lang)  # 暂无此类漫画
        category_id = int(getattr(self, "category"))
        category_name = CategoryEn.get_name_from_value(category_id).split("_")[0]
        comic_list = self.get_queryset(ComicInfo, {"category": category_id})
        if not comic_list:
            return EnumBase.get_status(622, CodeEn, lang)  # 暂无此类漫画
        redis_key = "comic_%s_%s" % (category_name, lang)
        result_comic_list = self.get_redis_context(redis_key)
        if not result_comic_list:
            mysql_re = self.get_mysql_context(comic_list, lang, is_pass_error=True)
            if isinstance(mysql_re, list):
                r.setex(redis_key, mysql_re, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
                result_comic_list = mysql_re
            else:
                return mysql_re
        obj, current_page, total_page = self.comics_list_paginator(result_comic_list, page)
        return ComicMethod.pack_success_data(success_list=list(obj), current_page=current_page,
                                             total_page=total_page)


class OwnPurchaseListViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            lang = getattr(self, "lang", "ms")
            page = getattr(self, "current_page", "1")
            email = getattr(self, "email")
            data = self.own_purchase_comics(email, lang, page)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def own_purchase_comics(self, email, lang, page):
        purchase_list = self.get_queryset(PurchaseAndFavorite, {"email": email, "status": 0}, perm_type="and")
        if not purchase_list:
            return EnumBase.get_status(631, CodeEn, lang)  # 该用户未购任何漫画
        comic_list = self.result_list_to_comic_list(purchase_list)
        result_comic_list = self.get_mysql_context(comic_list, lang, is_pass_error=True)
        obj, current_page, total_page = self.comics_list_paginator(result_comic_list, page)
        return ComicMethod.pack_success_data(success_list=list(obj), current_page=current_page,
                                             total_page=total_page)


class OwnCollectListViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    @set_attr
    def post(self, request):

        data = self._pre_check()
        if not isinstance(data, dict):
            lang = getattr(self, "lang", "ms")
            page = getattr(self, "current_page", "1")
            email = getattr(self, "email")
            data = self.own_collect_comics(email, lang, page)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def own_collect_comics(self, email, lang, page):
        favourite_list = self.get_queryset(PurchaseAndFavorite, {"email": email, "status": 1}, perm_type="and")
        if not favourite_list:
            # return EnumBase.get_status(631, CodeEn, lang)  # 该用户未购任何漫画
            favourite_list = []
        comic_list = self.result_list_to_comic_list(favourite_list)
        result_comic_list = self.get_mysql_context(comic_list, lang, is_pass_error=True)
        obj, current_page, total_page = self.comics_list_paginator(result_comic_list, page)
        return ComicMethod.pack_success_data(success_list=list(obj), current_page=current_page,
                                             total_page=total_page)


class OwnCollectPostViewSet(viewsets.ViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.update_own_collect()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def update_own_collect(self):
        email = getattr(self, "email")
        com_id = getattr(self, "comics_id")
        lang = getattr(self, "lang", "ms")
        base_obj = PurchaseAndFavorite.objects.filter(email=email)
        exit_com_list = base_obj.filter(status=1).values_list("com_id", flat=True)
        if int(com_id) in exit_com_list:
            base_obj.filter(com_id=com_id, status=1).update(status=2)
            return EnumBase.get_status(602, CodeEn, lang)
        elif base_obj.filter(status=2, com_id=com_id):
            base_obj.filter(status=2, com_id=com_id).update(status=1)
        else:
            PurchaseAndFavorite.objects.create(com_id=com_id, email=email, status=1)
        return EnumBase.get_status(601, CodeEn, lang)
            # return ComicMethod.pack_success_data()


class SearchListViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            q = getattr(self, "q", None)
            lang = getattr(self, "lang", "ms")
            page = getattr(self, "current_page", "1")
            data = self.search_comics_handler(q, lang, page)
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def search_comics_handler(self, q, lang, page):
        t = "%s_title" % lang
        if not q:
            result_hot_search_list = self.get_redis_context("hot_search", is_solidset=True)
            if result_hot_search_list:
                success_list = []
                for i in result_hot_search_list:
                    com_id = eval(i[0])
                    search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                    if isinstance(search_re, dict):
                        title = search_re.get("title").title()
                    else:
                        continue
                    success_list.append(title)
                    if len(success_list) >= 6:
                        break
                return ComicMethod.pack_success_data(success_list=success_list)
            else:
                return ComicMethod.pack_success_data(success_list=[])
        else:
            search_list = self.get_queryset(Search, {"%s__icontains" % t: q})
            if not search_list:
                return EnumBase.get_status(620, CodeEn, lang)  # 暂无此漫画
            comic_list = self.result_list_to_comic_list(search_list)
            result_comic_list = self.get_mysql_context(comic_list, lang, is_pass_error=True)
            hot_comics = result_comic_list[0]["comicsID"]
            r.zincrby("hot_search", hot_comics, 1)
            obj, current_page, total_page = self.comics_list_paginator(result_comic_list, page)
            return ComicMethod.pack_success_data(success_list=list(obj), current_page=current_page,
                                                 total_page=total_page)
