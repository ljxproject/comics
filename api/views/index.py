import itertools
import operator

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import ComicInfo, CategoryStatus, ComicStatus
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.helpers import r


@api_view(["GET"])
def get_index(request):
    """
    获取首页信息
    """
    lang = request.GET.get("lang") if request.GET.get("lang") else "en"
    # 从redis 获取
    index_list = r.get("comic_index_%s" % lang)
    category_list = []
    if not index_list:
        index_list = []
        # 从漫画信息表中筛选category=1,获得com_id
        edit_comic_list = ComicInfo.filter(category=1).order_by("-modified")[:4]
        # 从漫画信息表中筛选category=2 获得com_id
        fin_comic_list = ComicInfo.filter(category=2).order_by("-modified")[:4]  # todo 并无完结列表
        # 从漫画信息表中筛选category = 3 获得com_id
        trend_comic_list = ComicInfo.filter(category=3).order_by("-modified")[:4]
        # 从漫画信息表中筛选category = 10 获得com_id
        manhua_comic_list = ComicInfo.filter(category=10).order_by("-modified")[:4]
        # 从漫画信息表中筛选category = 11 获得com_id
        manga_comic_list = ComicInfo.filter(category=11).order_by("-modified")[:4]
        comic_list = list(itertools.chain(edit_comic_list, fin_comic_list, trend_comic_list,
                                          manhua_comic_list, manga_comic_list))
        for i in comic_list:
            com_id = i.com_id
            cover_img = i.my_com_cover_img
            status = {
                "code": i.status,
                "name": ComicStatus.get_name_from_value(i.status)
            }
            category = i.category
            # 根据com_id 查检索表
            search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
            if isinstance(search_re, dict):
                title = search_re.get("title")
                subtitle = search_re.get("subtitle")
            else:
                data = {
                    "status": search_re.value,
                    "msg": search_re.name.replace("_", " ").title(),
                }
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            index_dict = {"comicsID": com_id, "comicsTitle": title,
                          "comicsCover": cover_img, "comicsSubtitle": subtitle,
                          "comicsStatus": status, "categoryCode": category}
            index_list.append(index_dict)
        r.setex("comic_index_%s" % lang, index_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
    index_list = eval(index_list) if isinstance(index_list, bytes) else index_list
    for c in index_list:
        category_list.append(c["categoryCode"])
    category_list = list(set(category_list))
    category_dit = CategoryStatus.to_dict(category_list)
    category_dit = dict(sorted(category_dit.items(), key=operator.itemgetter(0), reverse=False))
    index_list = sorted(index_list, key=lambda x: x["categoryCode"])
    data = ComicMethod.pack_success_data(success_list=index_list, category=category_dit)
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
