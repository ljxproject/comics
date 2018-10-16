
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers import fuzzy_search_handler, r
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.models import Search


@api_view(["GET"])
def get_fuzzy_search_comics(request):
    """
    模糊查询
    接收q lang
    返回10个结果
    """
    q = request.GET.get("q")
    lang = request.GET.get("lang", "my")
    # 不存在则返回热搜榜
    if not q:
        re = r.zrange("hot_search", -7, -1, withscores=True)
        if re:
            if not lang or lang == "my":
                success_list = []
                for i in re:
                    com_id = eval(i[0])
                    title = Search.get(com_id=com_id).my_title
                    success_list.append(title)
                data = ComicMethod.pack_success_data(success_list=success_list[::-1])
        else:
            data = ComicMethod.pack_success_data(success_list=re)
    # q存在进行模糊查询
    else:
        comics_list_re = fuzzy_search_handler.create_comics_list(q, lang)
        success_list = comics_list_re
        data = ComicMethod.pack_success_data(success_list=success_list)
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)



