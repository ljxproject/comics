import os

from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from api.helpers import EnumBase
from api.helpers.code import CodeEn
from api.helpers.serializer import ComicsSuccessSerializer

from api.helpers.comic_method import ComicMethod
from api.models import ComicInfo, ImgResource


@api_view(["POST"])
def get_comics_detail(request):
    """
    获取漫画图片
    接收com_id chap_id email lang
    """
    email = request.data.get("email")
    com_id = request.data.get("comicsID")
    lang = request.data.get("lang", "ms")
    chap_id = request.data.get("chapterID")
    com = ComicInfo.filter(com_id=com_id)
    chap = ImgResource.filter(chap_id=chap_id, com_id=com_id)

    if not com:
        data = EnumBase.get_status(620, CodeEn, lang)  # 暂无此漫画
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    if not chap:
        data = EnumBase.get_status(621, CodeEn, lang)  # 该漫画暂无此章节
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    # 获取漫画内容表的基本信息,接收com_id,chap_id
    info_dict = ComicMethod.get_img_resource_info(com_id=com_id, lang=lang)
    info_list = sorted(info_dict.items(), key=lambda e: int(e[0]))
    chap_id_list_total = []
    for i in info_list:
        if isinstance(i[0], bytes):
            chap_id_list_total.append(str((eval(i[0]))))
        else:
            chap_id_list_total.append(str(i[0]))
    # 无用户则查漫画信息表,匹配chap_id与free_comic
    com = com.first()
    if com.status == 1003:
        chap_id_list = chap_id_list_total
    else:
        chap_id_list = [str(i + 1) for i in range(com.free_chapter)]
    # 有则在redis中查询用户章节权限,匹配chap_id与chap_list
    if email:
        email.lower()
        permission_re = ComicMethod.get_user_chapter_authority(email=email, com_id=com_id)
        permission_re = eval(permission_re) if isinstance(permission_re, bytes) else permission_re
        chap_id_list = list(set(chap_id_list + permission_re))
        chap_id_list = list(set(chap_id_list).intersection(set(chap_id_list_total)))
    if chap_id in chap_id_list:
        # 在redis查询img资源 返回url列表
        img_re = ComicMethod.get_one_img_resource(com_id=com_id, chap_id=chap_id, lang=lang)
        if not isinstance(img_re, list):
            data = EnumBase.get_status(660, CodeEn, lang)  # 未知错误
        else:
            img_list_path = img_re[0].get("%s_img_list_path" % lang)
            if not img_list_path:
                data = EnumBase.get_status(629, CodeEn, lang)  # 无该语言章节
            else:
                path = os.path.join(settings.MEDIA_ROOT, "img", img_list_path)
                img_list = os.listdir(path)  # 按序
                asc_img_list = sorted(img_list, key=lambda x: int(x[:-4]))
                p = Paginator(asc_img_list, 3)
                page = request.data.get("currentPage")
                total_page = p.num_pages

                if page and int(page) <= total_page:
                    success_list = p.page(int(page))
                    current_page = int(page)
                elif page and int(page) > total_page:
                    success_list = p.page(total_page)
                    current_page = total_page
                else:
                    success_list = p.page(1)
                    current_page = 1
                data = ComicMethod.pack_success_data(success_list=list(success_list), current_page=current_page,
                                                     total_page=total_page)
    else:
        data = EnumBase.get_status(630, CodeEn, lang)  # 该用户暂无此章节权限
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
