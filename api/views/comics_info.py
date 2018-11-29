from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import ComicInfo, ComicCoverImg
from api.helpers.code import CodeEn, ComicEn
from api.helpers import EnumBase, MyViewBackend, set_attr
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.views import ComicsListBaseView
from userapi.models import Comment, PurchaseAndFavorite


class ChapterInfoViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):
    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            data = self.chapter_list()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def chapter_list(self):
        lang = getattr(self, "lang", "ms")
        com_id = getattr(self, "comics_id")
        email = getattr(self, "email") if hasattr(self, "email") else None
        com = self.get_queryset(ComicInfo, {"com_id": com_id}).first()
        free_chapter = com.free_chapter
        # 获取漫画内容表的基本信息,接收com_id,chap_id
        info_dict = ComicMethod.get_img_resource_info(com_id=com_id, lang=lang)
        info_list = sorted(info_dict.items(), key=lambda e: int(e[0]))
        chapter_list = []
        chap_id_list_total = []
        for i in info_list:
            if isinstance(i[0], bytes):
                chap_id_list_total.append(str((eval(i[0]))))
            else:
                chap_id_list_total.append(str(i[0]))

        if com.status == 1003:
            chap_id_list = chap_id_list_total
        else:
            chap_id_list = [str(i + 1) for i in range(free_chapter)]
        # 判断是否有email
        if email:
            # 有则从权限列表中获取用户权限信息, 接收email
            permission_re = ComicMethod.get_user_chapter_authority(email=email, com_id=com_id)
            permission_re = eval(permission_re) if isinstance(permission_re, bytes) else permission_re
            chap_id_list = list(set(chap_id_list + permission_re))
            chap_id_list = list(set(chap_id_list).intersection(set(chap_id_list_total)))

        for i in range(len(info_list)):
            tmp = list(info_list[i])[1]
            if isinstance(tmp, bytes):
                result_dict = eval(tmp)[0]
            else:
                result_dict = tmp[0]
            chap_id = result_dict["chap_id"]
            price = result_dict["price"]
            chap_cover_img = result_dict["chap_cover_img"]
            if str(i + 1) in chap_id_list:
                chap_authority = 1
            else:
                chap_authority = 0  # 0 没购买
            chap_title = result_dict.get("%s_title" % lang)
            if not chap_title:
                chap_status = EnumBase.get_status(629, CodeEn, lang)  # this_chapter_has_not_localization
            else:
                chap_status = EnumBase.get_status(600, CodeEn, lang)  # success
            chap_path = result_dict["%s_img_list_path" % lang]
            chapter_dict = {"chapterID": chap_id, "chapterImg": chap_cover_img, "chapterPrice": price,
                            "chapterAuthority": chap_authority, "chapterTitle": chap_title,
                            "chapterPath": chap_path, "chapterStatus": chap_status}
            chapter_list.append(chapter_dict)
        return ComicMethod.pack_success_data(comics_free_chapter=free_chapter, comics_total_chapter=len(info_list),
                                             chapter_list=chapter_list)


# @api_view(["POST"])
# def get_comics_info(request):
#     """
#     获取漫画信息
#     接收com_id lang email
#     """
#     lang = request.data.get("lang", "en")
#     email = request.data.get("email")
#     com_id = request.data.get("comicsID")
#
#     # 判断com_id是否存在
#     com = ComicInfo.filter(com_id=com_id)
#     if not com:
#         data = EnumBase.get_status(620, CodeEn, lang)  # 暂无此漫画
#         serializer = ComicsSuccessSerializer(data)
#         return Response(serializer.data)
#     # 获取comics表数据
#     com = com.first()
#     com_cover_img = ComicCoverImg.get(com_id=com_id).values_list("%s_comic_cover_img" % lang, flat=True)[0]
#     free_chapter = com.free_chapter
#     total_chapter = com.total_chapter
#     status = EnumBase.get_status(com.status, ComicEn, lang)
#     modified = com.modified
#     # 从漫画检索表中获取漫画基本信息,接收language
#     search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
#     if isinstance(search_re, dict):
#         title = search_re.get("title")
#         author = search_re.get("author")
#         introduction = search_re.get("introduction")
#     else:
#         data = EnumBase.get_status(628, CodeEn, lang)  # 无该语言漫画错误
#         serializer = ComicsSuccessSerializer(data)
#         return Response(serializer.data)
#     # 获取漫画是否收藏
#     if email and PurchaseAndFavorite.filter(email=email.lower(), com_id=com_id, status=1):
#         comics_collection_status = 1
#     else:
#         comics_collection_status = 0
#     data = ComicMethod.pack_success_data(comics_title=title, comics_author=author,
#                                          comics_intro=introduction, comics_img=com_cover_img,
#                                          comics_free_chapter=free_chapter, comics_total_chapter=total_chapter,
#                                          comics_status=status, comics_modified=modified,
#                                          comics_collection_status=comics_collection_status)
#     serializer = ComicsSuccessSerializer(data)
#     return Response(serializer.data)


class ComicInfoViewSet(viewsets.ViewSet, MyViewBackend, ComicsListBaseView):

    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            data = self.get_comic()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def get_comic(self):
        com_id = getattr(self, "comics_id")
        lang = getattr(self, "lang", "ms")

        # 判断com_id是否存在
        com = ComicInfo.filter(com_id=com_id)
        if not com:
            data = EnumBase.get_status(620, CodeEn, lang)  # 暂无此漫画
            serializer = ComicsSuccessSerializer(data)
            return Response(serializer.data)
        # 获取comics表数据
        com = com.first()
        com_cover_img = ComicCoverImg.get(com_id=com_id).values_list("%s_comic_cover_img" % lang, flat=True)[0]
        free_chapter = com.free_chapter
        total_chapter = com.total_chapter
        status = EnumBase.get_status(com.status, ComicEn, lang)
        modified = com.modified
        # 从漫画检索表中获取漫画基本信息,接收language
        search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
        if isinstance(search_re, dict):
            title = search_re.get("title")
            author = search_re.get("author")
            introduction = search_re.get("introduction")
        else:
            data = EnumBase.get_status(628, CodeEn, lang)  # 无该语言漫画错误
            serializer = ComicsSuccessSerializer(data)
            return Response(serializer.data)
        comment_list = self.get_queryset(Comment, {"com_id": com_id, "is_delete": 0, "lang": lang},
                                         perm_type="and").order_by("-rate", "-created")[:5]
        if comment_list:
            comments_list = list(self.get_comment_list(comment_list))
        else:
            comments_list = []
        if hasattr(self, "email") and PurchaseAndFavorite.filter(email=getattr(self, "email").lower(), com_id=com_id,
                                                                 status=1):
            comics_collection_status = 1
        else:
            comics_collection_status = 0
        return ComicMethod.pack_success_data(comments_list=comments_list, comics_title=title, comics_author=author,
                                             comics_intro=introduction, comics_img=com_cover_img,
                                             comics_free_chapter=free_chapter, comics_total_chapter=total_chapter,
                                             comics_status=status, comics_modified=modified,
                                             comics_collection_status=comics_collection_status)
