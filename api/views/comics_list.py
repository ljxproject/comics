from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import ComicInfo, ComicStatus, Search
from api.helpers.code import Code
from api.helpers.comic_method import ComicMethod
from api.helpers import r
from api.helpers.serializer import ComicsSuccessSerializer
from userapi.models import PurchaseAndFavorite


@api_view(["GET"])
def get_edit_comics(request):
    """
    获取主编推荐列表
    接收lang
    """
    # 判断漫画列表是否存在主编推荐
    comic_list = ComicInfo.filter(category=1).order_by("-modified")
    if not comic_list:
        data = {
            "status": Code.category_do_not_exist.value,
            "msg": Code.category_do_not_exist.name.replace("_", " ").title(),
        }
    else:
        lang = request.GET.get("lang") if request.GET.get("lang") else "en"
        # 从redis 获取
        edit_comic_list = r.get("comic_edit_%s" % lang)
        if not edit_comic_list:
            edit_comic_list = []
            for i in comic_list:
                com_id = i.com_id
                cover_img = i.my_com_cover_img
                status = {
                    "code": i.status,
                    "name": ComicStatus.get_name_from_value(i.status)
                }
                # 根据com_id 查检索表
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title")
                    author = search_re.get("author")
                else:
                    data = {
                        "status": search_re.value,
                        "msg": search_re.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                edit_comic_list.append(comic_dict)
            r.setex("comic_edit_%s" % lang, edit_comic_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        edit_comic_list = eval(edit_comic_list) if isinstance(edit_comic_list, bytes) else edit_comic_list
        p = Paginator(edit_comic_list, 10)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_finish_comics(request):
    """
    获取完结推荐列表
    接收lang
    """
    # 判断漫画列表是否存在主编推荐
    comic_list = ComicInfo.filter(category=2).order_by("-modified")
    if not comic_list:
        data = {
            "status": Code.category_do_not_exist.value,
            "msg": Code.category_do_not_exist.name.replace("_", " ").title(),
        }
    else:
        lang = request.GET.get("lang") if request.GET.get("lang") else "en"
        # 从redis 获取
        finish_comic_list = r.get("comic_finish_%s" % lang)
        if not finish_comic_list:
            finish_comic_list = []
            for i in comic_list:
                com_id = i.com_id
                cover_img = i.my_com_cover_img
                status = {
                    "code": i.status,
                    "name": ComicStatus.get_name_from_value(i.status)
                }
                # 根据com_id 查检索表
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title")
                    author = search_re.get("author")
                else:
                    data = {
                        "status": search_re.value,
                        "msg": search_re.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                finish_comic_list.append(comic_dict)
            r.setex("comic_finish_%s" % lang, finish_comic_list, 24 * 60 * 60)
        finish_comic_list = eval(finish_comic_list) if isinstance(finish_comic_list, bytes) else finish_comic_list
        p = Paginator(finish_comic_list, 10)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_trend_comics(request):
    """
    获取热门推荐列表
    接收lang
    """
    # 判断漫画列表是否存在主编推荐
    comic_list = ComicInfo.filter(category=3).order_by("-modified")
    if not comic_list:
        data = {
            "status": Code.category_do_not_exist.value,
            "msg": Code.category_do_not_exist.name.replace("_", " ").title(),
        }
    else:
        lang = request.GET.get("lang") if request.GET.get("lang") else "en"
        # 从redis 获取
        trend_comic_list = r.get("comic_trend_%s" % lang)
        if not trend_comic_list:
            trend_comic_list = []
            for i in comic_list:
                com_id = i.com_id
                cover_img = i.my_com_cover_img
                status = {
                    "code": i.status,
                    "name": ComicStatus.get_name_from_value(i.status)
                }
                # 根据com_id 查检索表
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title")
                    author = search_re.get("author")
                else:
                    data = {
                        "status": search_re.value,
                        "msg": search_re.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                trend_comic_list.append(comic_dict)
            r.setex("comic_trend_%s" % lang, trend_comic_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        trend_comic_list = eval(trend_comic_list) if isinstance(trend_comic_list, bytes) else trend_comic_list
        p = Paginator(trend_comic_list, 10)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_manhua_comics(request):
    """
    获取中漫推荐列表
    接收lang
    """
    # 判断漫画列表是否存在主编推荐
    comic_list = ComicInfo.filter(category=10).order_by("-modified")
    if not comic_list:
        data = {
            "status": Code.category_do_not_exist.value,
            "msg": Code.category_do_not_exist.name.replace("_", " ").title(),
        }
    else:
        lang = request.GET.get("lang") if request.GET.get("lang") else "en"
        # 从redis 获取
        manhua_comic_list = r.get("comic_manhua_%s" % lang)
        if not manhua_comic_list:
            manhua_comic_list = []
            for i in comic_list:
                com_id = i.com_id
                cover_img = i.my_com_cover_img
                status = {
                    "code": i.status,
                    "name": ComicStatus.get_name_from_value(i.status)
                }
                # 根据com_id 查检索表
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title")
                    author = search_re.get("author")
                else:
                    data = {
                        "status": search_re.value,
                        "msg": search_re.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                manhua_comic_list.append(comic_dict)
            r.setex("comic_manhua_%s" % lang, manhua_comic_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        manhua_comic_list = eval(manhua_comic_list) if isinstance(manhua_comic_list, bytes) else manhua_comic_list
        p = Paginator(manhua_comic_list, 10)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_manga_comics(request):
    """
    获取中漫推荐列表
    接收lang
    """
    # 判断漫画列表是否存在主编推荐
    comic_list = ComicInfo.filter(category=11).order_by("-modified")
    if not comic_list:
        data = {
            "status": Code.category_do_not_exist.value,
            "msg": Code.category_do_not_exist.name.replace("_", " ").title(),
        }
    else:
        lang = request.GET.get("lang") if request.GET.get("lang") else "en"
        # 从redis 获取
        manga_comic_list = r.get("comic_manga_%s" % lang)
        if not manga_comic_list:
            manga_comic_list = []
            for i in comic_list:
                com_id = i.com_id
                cover_img = i.my_com_cover_img
                status = {
                    "code": i.status,
                    "name": ComicStatus.get_name_from_value(i.status)
                }
                # 根据com_id 查检索表
                search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
                if isinstance(search_re, dict):
                    title = search_re.get("title")
                    author = search_re.get("author")
                else:
                    data = {
                        "status": search_re.value,
                        "msg": search_re.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                manga_comic_list.append(comic_dict)
            r.setex("comic_manga_%s" % lang, manga_comic_list, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        manga_comic_list = eval(manga_comic_list) if isinstance(manga_comic_list, bytes) else manga_comic_list
        p = Paginator(manga_comic_list, 10)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_own_purchase_comics(request):
    """
    获取用户购买列表
    接收email lang
    """
    email = request.GET.get("email")
    lang = request.GET.get("lang") if request.GET.get("lang") else "my"
    own_purchase_list = []
    # 从redis中获取用户购买列表
    comic_list = list(PurchaseAndFavorite.filter(email=email, status=0).values_list("com_id", flat=True))
    if not comic_list:
        data = {
            "status": Code.it_seems_you_have_not_any_purchased_comics_yet.value,
            "msg": Code.it_seems_you_have_not_any_purchased_comics_yet.name.replace("_", " ").title()
        }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    for i in comic_list:
        com_id = i
        cover_img = ComicInfo.get(com_id=com_id).my_com_cover_img
        status = {
            "code": ComicInfo.get(com_id=com_id).status,
            "name": ComicStatus.get_name_from_value(ComicInfo.get(com_id=com_id).status)
        }
        search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
        if isinstance(search_re, dict):
            title = search_re.get("title")
            author = search_re.get("author")
        else:
            continue
        comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                      "comicsCover": cover_img, "comicsStatus": status}
        own_purchase_list.append(comic_dict)
    # 对结果进行分页
    p = Paginator(own_purchase_list, 15)
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
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def get_own_favorite_comics(request):
    pass


@api_view(["GET"])
def get_search_comics(request):
    """
    获取收索列表
    接收 q lang page
    """
    # 判断q是否存在
    q = request.GET.get("q")
    lang = request.GET.get("lang")
    # 不存在则返回热搜榜
    if not q:
        re = r.zrange("hot_search", -7, -1, withscores=True)
        if re:
            if not lang or lang == "my":
                success_list = []
                for i in re:
                    com_id = eval(i[0])
                    title = Search.get(com_id=com_id).my_title.title()
                    success_list.append(title)
                data = ComicMethod.pack_success_data(success_list=success_list)
        else:
            data = ComicMethod.pack_success_data(success_list=re)
    # 判断lang是否存在,不存在返回无该语言漫画错误
    else:
        if not lang or lang == "my":
            # 存在,则根据lang查search表
            search_list = Search.filter(my_title__icontains=q)
            if not search_list:
                data = {
                    "status": Code.comics_not_found.value,
                    "msg": Code.comics_not_found.name.replace("_", " ").title(),
                }
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            comics_list = []
            for i in search_list:
                com_id = i.com_id
                title = i.my_title
                author = i.my_author
                cover_img = ComicInfo.get(com_id=com_id).my_com_cover_img
                status = {
                    "code": ComicInfo.get(com_id=com_id).status,
                    "name": ComicStatus.get_name_from_value(ComicInfo.get(com_id=com_id).status)
                }
                comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                              "comicsCover": cover_img, "comicsStatus": status}
                comics_list.append(comic_dict)
            # 在redis热搜榜添加第一个comic
            hot_comics = comics_list[0]["comicsID"]
            r.zincrby("hot_search", hot_comics, 1)
            # 对结果进行分页
            p = Paginator(comics_list, 10)
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
                "status": Code.this_comics_has_not_localization.value,
                "msg": Code.this_comics_has_not_localization.name.replace("_", " ").title(),
            }
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
