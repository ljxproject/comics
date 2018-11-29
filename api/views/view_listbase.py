import time

from adminx.helpers import MyPaginator
from api.helpers import r, EnumBase
from api.helpers.code import ComicEn, CodeEn
from api.models import ComicCoverImg, ComicInfo
from api.helpers.comic_method import ComicMethod
from userapi.models import User


class ComicsListBaseView(object):
    list_per_page = 10

    def get_queryset(self, model, perm_dict, perm_type=None):
        key_list = perm_dict.keys()
        if not perm_type:
            if len(key_list) > 1:
                raise IndexError("perm_dict length must be one")
            else:
                return model.filter(**perm_dict)
        elif perm_type == "and":
            queryset = model
            for key in key_list:
                queryset = queryset.filter(**{key: perm_dict[key]})
        elif perm_type == "or":
            queryset = []
            for key in key_list:
                _queryset = model.filter(**{key: perm_dict[key]})
                for i in _queryset:
                    queryset.append(i)
        else:
            raise ValueError("invalid perm")
        return queryset

    def get_redis_context(self, key, is_solidset=None):
        if is_solidset:
            redis_re = r.zrange(key, 0, -1, withscores=True)
            if redis_re:
                return redis_re
        else:
            redis_re = r.get(key)
            if redis_re:
                return eval(redis_re)
        return None

    def get_mysql_context(self, comic_list, lang, is_pass_error=None):
        result_comic_list = []
        for i in comic_list:
            com_id = i.com_id
            status = EnumBase.get_status(i.status, ComicEn, lang)
            search_re = ComicMethod.get_comic_base_info(lang=lang, com_id=com_id)
            if isinstance(search_re, dict):
                title = search_re.get("title")
                author = search_re.get("author")
            else:
                if is_pass_error:
                    continue
                return EnumBase.get_status(628, CodeEn, lang)  # 无该语言漫画错误
            cover_img = ComicCoverImg.get(com_id=com_id).values_list("%s_comic_cover_img" % lang, flat=True)[0]
            comic_dict = {"comicsID": com_id, "comicsTitle": title, "comicsAuthor": author,
                          "comicsCover": cover_img, "comicsStatus": status}
            result_comic_list.append(comic_dict)
        return result_comic_list

    def get_category_id(self, cls, key):
        return EnumBase.get_status_obj(cls, key).value

    def comics_list_paginator(self, result_comic_list, page):
        p = MyPaginator(result_comic_list, self.list_per_page)
        total_page = p.get_total_page()
        if int(page) > total_page:
            page = total_page
        obj = p.get_p_obj(page)
        current_page = int(page) if page else 1
        return obj, current_page, total_page

    def result_list_to_comic_list(self, result_list):
        comic_list = []
        for i in result_list:
            com_id = i.com_id
            queryset = self.get_queryset(ComicInfo, {"com_id": com_id})
            for comic in queryset:
                comic_list.append(comic)
        return comic_list

    def get_comment_list(self, comment_list):
        result_list = []
        for i in comment_list:
            title = i.title
            content = i.content
            rate = i.rate
            email = i.email
            date = i.created
            name = User.get(email=email).name
            cid = i.id
            t = time.mktime(date.timetuple())
            comment_dict = {"id": cid, "title": title, "content": content, "rate": rate, "nickname": name,
                            "date": t}
            result_list.append(comment_dict)
        return result_list
