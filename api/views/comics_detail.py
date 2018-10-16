import os

from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from api.helpers.serializer import ComicsSuccessSerializer

from api.helpers.code import Code
from api.helpers.comic_method import ComicMethod
from api.models import ComicInfo


@api_view(["GET"])
def get_comics_detail(request, com_id, chap_id):
    """
    获取漫画图片
    接收com_id chap_id email lang
    """
    email = request.GET.get("email")
    lang = request.GET.get("lang") if request.GET.get("lang") else "en"
    com = ComicInfo.get(com_id=com_id)
    # 无用户则查漫画信息表,匹配chap_id与free_comic
    if com.status == 1003:
        chap_id_list = [str(i + 1) for i in range(com.total_chapter)]
    else:
        chap_id_list = [str(i + 1) for i in range(com.free_chapter)]
    # 有则在redis中查询用户章节权限,匹配chap_id与chap_list
    if email:
        permission_re = ComicMethod.get_user_chapter_authority(email=email, com_id=com_id)
        chap_id_list = list(
            set(chap_id_list + eval(permission_re)) if isinstance(permission_re, bytes) else permission_re)
    if chap_id in chap_id_list:
        # 在redis查询img资源 返回url列表
        img_re = ComicMethod.get_one_img_resource(com_id=com_id, chap_id=chap_id)
        if not isinstance(img_re, list):
            data = {
                "status": img_re.value,
                "msg": img_re.name.replace("_", " ").title(),
            }
        else:
            if lang == "my" or lang == "en":
                img_list_path = img_re[0]["my_img_list_path"]
                path = os.path.join(settings.MEDIA_ROOT, "img", img_list_path)
                img_list = os.listdir(path)  # 按序
                asc_img_list = sorted(img_list, key=lambda x: int(x[:-4]))
                p = Paginator(asc_img_list, 3)
                page = request.GET.get("currentPage")
                if page:
                    success_list = p.page(page)
                    current_page = int(page)
                else:
                    success_list = p.page(1)
                    current_page = 1
                total_page = p.num_pages
                data = ComicMethod.pack_success_data(success_list=list(success_list), current_page=current_page,
                                                     total_page=total_page)
            else:
                data = {
                    "status": Code.this_chapter_has_not_localization.value,
                    "msg": Code.this_chapter_has_not_localization.name.replace("_", " ").title(),
                }
    else:
        data = {
            "status": Code.this_chapter_has_not_been_purchased.value,
            "msg": Code.this_chapter_has_not_been_purchased.name.replace("_", " ").title(),
        }
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
