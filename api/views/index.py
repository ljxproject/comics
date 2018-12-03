import itertools
import operator

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import ComicInfo, ComicCoverImg, Category
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.helpers import r, EnumBase, set_attr, MyViewBackend
from api.helpers.code import ComicEn, CategoryEn, CodeEn


# @api_view(["POST"])
# def get_index(request):
#     """
#     获取首页信息
#     """
#     lang = request.data.get("lang", "ms")
#     if lang == "en":
#         lang = "ms"
#     # 从redis 获取
#     index_list = r.get("comic_index_%s" % lang)
#     category_list = []
#     if not index_list:
#         index_list = []
#         # 从漫画信息表中筛选category=1,获得com_id
#         edit_comic_list = ComicInfo.filter(category=1).order_by("-modified")[:4]
#         # 从漫画信息表中筛选category=2 获得com_id
#         fin_comic_list = ComicInfo.filter(category=2).order_by("-modified")[:4]  # todo 并无完结列表
#         # 从漫画信息表中筛选category = 3 获得com_id
#         trend_comic_list = ComicInfo.filter(category=3).order_by("-modified")[:4]
#         # 从漫画信息表中筛选category = 10 获得com_id
#         manhua_comic_list = ComicInfo.filter(category=10).order_by("-modified")[:4]
#         # 从漫画信息表中筛选category = 11 获得com_id
#         manga_comic_list = ComicInfo.filter(category=11).order_by("-modified")[:4]
#         comic_list = list(itertools.chain(edit_comic_list, fin_comic_list, trend_comic_list,
#                                           manhua_comic_list, manga_comic_list))
#         for i in comic_list:
#             com_id = i.com_id
#             status = EnumBase.get_status(i.status, ComicEn, lang)
#             category = i.category
#             # 根据com_id 查检索表
#             search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
#             if isinstance(search_re, dict):
#                 title = search_re.get("title")
#                 subtitle = search_re.get("subtitle")
#             else:
#                 # data = EnumBase.get_status(628, CodeEn, lang)  # 无该语言漫画错误
#                 # serializer = ComicsSuccessSerializer(data)
#                 # return Response(serializer.data)
#                 continue
#             cover_img = ComicCoverImg.get(com_id=com_id).values_list("%s_comic_cover_img" % lang, flat=True)[0]
#             index_dict = {"comicsID": com_id, "comicsTitle": title,
#                           "comicsCover": cover_img, "comicsSubtitle": subtitle,
#                           "comicsStatus": status, "categoryCode": category}
#             index_list.append(index_dict)
#         r.setex("comic_index_%s" % lang, index_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
#     index_list = eval(index_list) if isinstance(index_list, bytes) else index_list
#     for c in index_list:
#         category_list.append(c["categoryCode"])
#     category_list = list(set(category_list))
#     category_dit = {i: EnumBase.get_status_default_name(i, CategoryEn) for i in category_list}
#     category_dit = dict(sorted(category_dit.items(), key=operator.itemgetter(0), reverse=False))
#     index_list = sorted(index_list, key=lambda x: x["categoryCode"])
#     data = ComicMethod.pack_success_data(success_list=index_list, category=category_dit)
#     serializer = ComicsSuccessSerializer(data)
#     return Response(serializer.data)


from api.views import ComicsListBaseView


class IndexComicsListViewSet(viewsets.ViewSet, ComicsListBaseView, MyViewBackend):
    key_list = [{"category": 1}, {"category": 2}, {"category": 3}, {"category": 10}, {"category": 11}]
    com_l = []
    index_list = []
    length = 4
    exist_com_id_list = []
    pass_com = 0
    qs = None
    invalid_list = []

    def _del(self):
        self.index_list = []
        self.com_l = []
        self.exist_com_id_list = []
        self.invalid_list = []
        self.pass_com = 0
        self.qs = None

    def category_model_handel(self, parm_dict):
        if not self.qs:
            self.qs = self.get_queryset(Category, parm_dict)
        parm_dict = self.get_new_com(self.qs)
        c_l = self.get_queryset(ComicInfo, parm_dict)
        return c_l

    def get_new_com(self, qs):
        com_id_list = []
        for i in qs:
            com_id = i.com_id
            if com_id in self.exist_com_id_list or com_id in self.invalid_list:
                continue
            com_id_list.append(com_id)
        parm_dict = {"com_id__in": com_id_list}
        return parm_dict

    def comic_model_handel(self, parm_dict):
        if not self.qs:
            self.qs = self.get_queryset(ComicInfo, parm_dict)
        parm_dict = self.get_new_com(self.qs)
        c_l = self.get_queryset(ComicInfo, parm_dict)
        return c_l

    def get_com_l(self, su, eu, f_k, f_v, model):
        if model is Category:
            c_l = self.category_model_handel({"%s" % f_k: f_v}).order_by("-modified")[0:eu - su]
        else:
            c_l = self.comic_model_handel({"%s" % f_k: f_v}).order_by("-modified")[0:eu - su]
        com_d = {f_v: {"f_k": f_k, "c_l": c_l, "nu": eu, "model": model}}
        self.com_l.append(com_d)

    def get_key(self, i):
        f_v = list(i.values())[0]
        f_k = list(i.keys())[0]
        model = Category if f_k == "category" and f_v >= 10 else ComicInfo
        self.get_com_l(0, self.length, f_k, f_v, model)

    def key_signal(self):
        for i in self.key_list:
            yield i

    @set_attr
    def post(self, request):

        self._del()
        if self.is_valid_lang():
            data = self.index_handler()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def index_handler(self):
        res = self.key_signal()
        lang = getattr(self, "lang", "ms")
        category_list = []
        self.index_list = r.get("comic_index_%s" % lang)
        if not self.index_list:
            self.index_list = []
            while True:
                self.pass_com = 0
                if self.com_l:
                    com_d = self.com_l.pop()
                    for k, v in com_d.items():
                        f_v = k
                        f_k = v["f_k"]
                        su = v["nu"]
                        o = v["c_l"]
                        model = v["model"]
                        for i in o:
                            com_id = i.com_id
                            search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                            if isinstance(search_re, dict):
                                title = search_re.get("title")
                                subtitle = search_re.get("subtitle")
                                cover_img = \
                                    ComicCoverImg.get(com_id=com_id).values_list("%s_comic_cover_img" % lang,
                                                                                 flat=True)[0]
                                status = EnumBase.get_status(i.status, ComicEn, lang)
                            else:
                                self.pass_com += 1
                                self.invalid_list.append(com_id)
                                continue
                            index_dict = {"comicsID": com_id, "comicsTitle": title,
                                          "comicsSubtitle": subtitle, "comicsCover": cover_img,
                                          "comicsStatus": status, "categoryCode": f_v}
                            self.index_list.append(index_dict)
                            self.exist_com_id_list.append(com_id)
                            self.exist_com_id_list = list(set(self.exist_com_id_list))

                if self.pass_com:
                    self.get_com_l(su, su + self.pass_com, f_k, f_v, model)
                if not self.com_l:
                    try:
                        self.invalid_list = []
                        self.qs = None
                        o = res.__next__()
                        self.get_key(o)
                    except:
                        break
            r.setex("comic_index_%s" % lang, self.index_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)

        self.index_list = eval(self.index_list) if isinstance(self.index_list, bytes) else self.index_list
        for c in self.index_list:
            category_list.append(c["categoryCode"])
        category_list = list(set(category_list))
        # category_dit = {i: EnumBase.get_status_default_name(i, CategoryEn) for i in category_list}
        category_dit = {}
        for i in category_list:
            if i >= 1000:
                category_dit[i] = EnumBase.get_status(i, ComicEn, lang)["msg"]
            else:
                category_dit[i] = EnumBase.get_status(i, CategoryEn, lang)["msg"]
        category_dit = dict(sorted(category_dit.items(), key=operator.itemgetter(0), reverse=False))
        self.index_list = sorted(self.index_list, key=lambda x: x["categoryCode"])
        data = ComicMethod.pack_success_data(success_list=self.index_list, category=category_dit)
        return data
