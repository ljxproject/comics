from api.helpers import EnumBase, attr_to_hump
from api.helpers.code import CodeEn
from api.helpers import r
from userapi.models import Permission
from api.models import Search, ImgResource, ComicInfo


class ComicMethod(object):
    @staticmethod
    def get_comic_base_info(**kwargs):
        """从漫画检索表中获取漫画基本信息
            接收language,
        """
        base_info = Search.get(com_id=kwargs.get("com_id")).__dict__
        lang = kwargs.get('lang')
        t = "%s_title" % lang
        a = "%s_author" % lang
        s = "%s_subtitle" % lang
        i = "%s_introduction" % lang
        if base_info.get(t):
            title = base_info.get(t, "")
            author = base_info.get(a, "")
            subtitle = base_info.get(s, "")
            introduction = base_info.get(i, "")
            return locals()
        else:
            # return Code.this_comics_has_not_localization
            return Exception

    @staticmethod
    def get_user_chapter_authority(**kwargs):
        """从权限列表中获取用户权限信息
            接收email
        """
        email = kwargs.get("email")
        com_id = kwargs.get("com_id")
        # 查询redis
        chap_id_list = r.hget("%s_authority" % email, "%s" % str(com_id))
        if not chap_id_list:
            lis = Permission.filter(email=email, com_id=com_id)
            com = ComicInfo.get(com_id=com_id)
            chap_id_list_free = [str(i + 1) for i in range(com.free_chapter)]
            chap_id_list_cost = [str(i.chap_id) for i in lis]
            chap_id_list = list(set(chap_id_list_cost).difference(set(chap_id_list_free)))
            r.hset("%s_authority" % email, "%s" % str(com_id), chap_id_list)
            r.expire("%s_authority" % email, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        return chap_id_list

    @staticmethod
    def get_img_resource_info(**kwargs):
        """获取漫画内容表的基本信息
            接收com_id
        """
        com_id = kwargs.get("com_id")
        lang = kwargs.get("lang")

        info_dict = r.hgetall("%s_%s_resource_info" % (str(kwargs.get("com_id")), lang))
        if not info_dict:
            p = r.pipeline()
            # lis = ImgResource.filter(com_id=com_id)
            lis = ComicMethod.get_chap_list_by_lang(com_id, lang=lang)
            info_dict = {}
            for i in lis:
                info_list = []
                _d = {}
                for k, v in vars(i).items():
                    if not k.startswith("_"):
                        _d[k] = v
                info_list.append(_d)
                p.hset("%s_%s_resource_info" % (str(kwargs.get("com_id")), lang), "%s" % str(i.chap_id), info_list)
                info_dict[i.chap_id] = info_list
            p.expire("%s_%s_resource_info" % (str(kwargs.get("com_id")), lang),
                     24 * 60 * 60).execute()  # todo 过期时间 24*60*60(一天)
        return info_dict

    @staticmethod
    def get_one_img_resource(**kwargs):
        """
        保存漫画内容表单个章节信息
        接收 chap_id com_id
        """
        com_id = kwargs.get("com_id")
        chap_id = kwargs.get("chap_id")
        lang = kwargs.get("lang")
        info_list = r.hget("%s_%s_resource_info" % (str(kwargs.get("com_id")), lang), "%s" % str(chap_id))
        if not info_list:
            info_dict = ComicMethod.get_img_resource_info(com_id=com_id, lang=lang)
            k, v = zip(*info_dict.items())
            typ = set(map(type, list(k)))
            if len(typ) == 1 and isinstance(list(k)[0], bytes):
                k_l = list(map(eval, list(k)))
                k_v = list(map(eval, list(v)))
                re_dict = dict(zip(k_l, k_v))
            elif len(typ) == 1 and isinstance(list(k)[0], int):
                re_dict = info_dict
            else:
                return None
            info_list = re_dict[int(chap_id)]
        return eval(info_list) if isinstance(info_list, bytes) else info_list

    @staticmethod
    def pack_success_data(**kwargs):
        data = {
            "status": 600,
            "msg": EnumBase.get_status_default_name(600, CodeEn),  # 成功
        }
        for k, v in kwargs.items():
            data[attr_to_hump(k)] = v
        return data

    @staticmethod
    def get_chap_list_by_lang(com_id, lang, is_free=None):
        """获取对应语言的章节列表"""
        img_base_obj = ImgResource.objects.filter(com_id=com_id)
        pre = {"%s_title" % lang: None}
        img_obj = img_base_obj.exclude(**pre)
        # if is_free:
        #     img_obj = img_obj.exclude(price="0.00")
        # chap_id_list = []
        # for i in img_obj:
        #     chap_id_list.append(i.chap_id)
        # return chap_id_list
        return img_obj
