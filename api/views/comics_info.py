from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import ComicInfo, ComicStatus
from api.helpers.code import Code
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer


@api_view(["GET"])
def get_comics_info(request, com_id):
    """
    获取漫画信息
    接收com_id lang email
    """
    # 判断com_id是否存在
    try:
        com = ComicInfo.get(com_id=com_id)
    except:
        data = {
            "status": Code.comics_not_found.value,
            "msg": Code.comics_not_found.name.replace("_", " ").title(),
        }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    else:
        # 获取comics表数据
        my_com_cover_img = com.my_com_cover_img
        free_chapter = com.free_chapter
        total_chapter = com.total_chapter
        status = {
            "status": com.status,
            "msg": ComicStatus.get_name_from_value(com.status)
        }
        modified = com.modified
        # 从漫画检索表中获取漫画基本信息,接收language
        lang = request.GET.get("lang") if request.GET.get("lang") else "my"
        search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
        if isinstance(search_re, dict):
            title = search_re.get("title")
            author = search_re.get("author")
            introduction = search_re.get("introduction")
        else:
            data = {
                "status": search_re.value,
                "msg": search_re.name.replace("_", " ").title(),
            }
            serializer = ComicsSuccessSerializer(data)
            return Response(serializer.data)
        # 获取漫画内容表的基本信息,接收com_id,chap_id
        info_dict = ComicMethod.get_img_resource_info(com_id=com_id)
        info_list = sorted(info_dict.items(), key=lambda e: int(e[0]))
        chapter_list = []
        if com.status == 1003:
            chap_id_list = [str(i + 1) for i in range(total_chapter)]
        else:
            chap_id_list = [str(i + 1) for i in range(free_chapter)]
        # 判断是否有email
        if request.GET.get("email"):
            # 有则从权限列表中获取用户权限信息, 接收email
            permission_re = ComicMethod.get_user_chapter_authority(email=request.GET.get("email"), com_id=com_id)
            chap_id_list = list(
                set(chap_id_list + eval(permission_re)) if isinstance(permission_re, bytes) else permission_re)
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
            chap_path = result_dict["%s_img_list_path" % lang]
            chap_title = result_dict.get("%s_title" % lang)
            if not chap_title:
                chap_status = {
                    "status": Code.this_chapter_has_not_localization.value,
                    "msg": Code.this_chapter_has_not_localization.name.replace("_", " ").title(),
                }
            else:
                chap_status = {
                    "status": Code.success.value,
                    "msg": Code.success.name,
                }
            chapter_dict = {"chapterID": chap_id, "chapterImg": chap_cover_img, "chapterPrice": price,
                            "chapterAuthority": chap_authority, "chapterTitle": chap_title,
                            "chapterPath": chap_path, "chapterStatus": chap_status}
            chapter_list.append(chapter_dict)
        data = ComicMethod.pack_comic_data(chapter_list=chapter_list, title=title, author=author,
                                           introduction=introduction, my_com_cover_img=my_com_cover_img,
                                           free_chapter=free_chapter, total_chapter=total_chapter,
                                           status=status, modified=modified)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
