from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers import fuzzy_search_handler, r, EnumBase
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.models import Search


@api_view(["POST"])
def get_fuzzy_search_comics(request):
    """
    模糊查询
    接收q lang
    返回6个结果
    """
    q = request.data.get("q")
    lang = request.data.get("lang", "ms")
    t = "%s_title" % lang
    field_list = []
    for field in Search._meta.fields:
        field_list.append(field.name)
    if t not in field_list:
        data = EnumBase.get_status(620, CodeEn, lang)  # 暂无此漫画
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    # 不存在则返回热搜榜
    if not q:
        re = r.zrange("hot_search", 0, -1, withscores=True)
        if re:
            success_list = []
            for i in re:
                com_id = eval(i[0])
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title").title()
                else:
                    continue
                success_list.append(title)
                if len(success_list) >= 6:
                    break
            data = ComicMethod.pack_success_data(success_list=success_list)
        else:
            data = ComicMethod.pack_success_data(success_list=re)
    # q存在进行模糊查询
    else:
        success_list = fuzzy_search_handler.create_comics_list(q, lang)
        data = ComicMethod.pack_success_data(success_list=success_list)
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
