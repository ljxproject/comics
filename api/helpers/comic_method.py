from rest_framework.response import Response

from api.helpers.code import Code
from api.helpers.serializer import ComicsSuccessSerializer
from api.models import Search, ImgResource, ComicInfo
from api.helpers import r
from userapi.models import Permission


class ComicMethod(object):
    @staticmethod
    def get_comic_base_info(**kwargs):
        """从漫画检索表中获取漫画基本信息
            接收language,
        """
        base_info = Search.get(com_id=kwargs.get("com_id"))
        if kwargs.get("lang") == "my" or kwargs.get("lang") == "en":
            title = base_info.my_title
            author = base_info.my_author
            subtitle = base_info.my_subtitle
            introduction = base_info.my_introduction
            return locals()
        else:
            return Code.this_comics_has_not_localization

    @staticmethod
    def get_user_chapter_authority(**kwargs):
        """从权限列表中获取用户权限信息
            接收email
        """
        email = kwargs.get("email")
        # 查询redis
        chap_id_list = r.hget("%s_authority" % email, "%s" % str(kwargs.get("com_id")))
        if not chap_id_list:
            lis = Permission.filter(email=email, com_id=kwargs.get("com_id"))
            com = ComicInfo.get(com_id=kwargs.get("com_id"))
            chap_id_list_free = [str(i + 1) for i in range(com.free_chapter)]
            chap_id_list_cost = [str(i.chap_id) for i in lis]
            chap_id_list = list(set(chap_id_list_cost).difference(set(chap_id_list_free)))
            r.hset("%s_authority" % email, "%s" % str(kwargs.get("com_id")), chap_id_list)
            r.expire("%s_authority" % email, 24*60*60)  # todo 过期时间 24*60*60(一天)
        return chap_id_list

    @staticmethod
    def get_img_resource_info(**kwargs):
        """获取漫画内容表的基本信息
            接收com_id
        """
        info_dict = r.hgetall("%s_resource_info" % str(kwargs.get("com_id")))
        if not info_dict:
            p = r.pipeline()
            lis = ImgResource.filter(com_id=kwargs.get("com_id"))
            info_dict = {}
            for i in lis:
                info_list = []
                _d = {}
                for k, v in vars(i).items():
                    if not k.startswith("_"):
                        _d[k] = v
                info_list.append(_d)
                p.hset("%s_resource_info" % str(kwargs.get("com_id")), "%s" % str(i.chap_id), info_list)
                info_dict[i.chap_id] = info_list
            p.expire("%s_resource_info" % str(kwargs.get("com_id")), 24*60*60).execute()  # todo 过期时间 24*60*60(一天)
        return info_dict

    @staticmethod
    def get_one_img_resource(**kwargs):
        """
        保存漫画内容表单个章节信息
        接收 chap_id com_id
        """
        com_id = kwargs.get("com_id")
        chap_id = kwargs.get("chap_id")
        info_list = r.hget("%s_resource_info" % str(com_id), "%s" % str(chap_id))
        if not info_list:
            info_dict = ComicMethod.get_img_resource_info(com_id=com_id)
            k, v = zip(*info_dict.items())
            typ = set(map(type, list(k)))
            if len(typ) == 1 and isinstance(list(k)[0], bytes):
                k_l = list(map(eval, list(k)))
                k_v = list(map(eval, list(v)))
                re_dict = dict(zip(k_l, k_v))
            elif len(typ) == 1 and isinstance(list(k)[0], int):
                re_dict = info_dict
            else:
                data = {
                    "status": Code.unknown_error.value,
                    "msg": Code.unknown_error.name.replace("_", " ").title(),
                }
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            info_list = re_dict[int(chap_id)]
        return eval(info_list) if isinstance(info_list, bytes) else info_list

    @staticmethod
    def pack_comic_data(**kwargs):
        chapter_list = kwargs.get("chapter_list")
        title = kwargs.get("title")
        author = kwargs.get("author")
        my_com_cover_img = kwargs.get("my_com_cover_img")
        introduction = kwargs.get("introduction")
        modified = kwargs.get("modified")
        status = kwargs.get("status")
        free_chapter = kwargs.get("free_chapter")
        total_chapter = kwargs.get("total_chapter")
        data = {
            "status": Code.success.value,
            "msg": Code.success.name,
            "comicsTitle": title,
            "comicsAuthor": author,
            "comicsImg": my_com_cover_img,
            "comicsIntro": introduction,
            "comicsModified": modified,
            "comicsStatus": status,
            "comicsFreeChapter": free_chapter,
            "comicsTotalChapter": total_chapter,
            "chapterList": chapter_list
        }
        return data

    @staticmethod
    def pack_success_data(**kwargs):
        data = {
            "status": Code.success.value,
            "msg": Code.success.name
        }
        if kwargs.get("success_list") == [] or kwargs.get("success_list"):
            data["comicsList"] = kwargs.get("success_list")
        if kwargs.get("category"):
            data["category"] = kwargs.get("category")
        if kwargs.get("current_page"):
            data["currentPage"] = kwargs.get("current_page")
        if kwargs.get("total_page"):
            data["totalPage"] = kwargs.get("total_page")
        if kwargs.get("session_key"):
            data["sessionKey"] = kwargs.get("session_key")
        if kwargs.get("tx_id"):
            data["txID"] = kwargs.get("tx_id")
        if kwargs.get("email"):
            data["email"] = kwargs.get("email")
        return data

    @staticmethod
    def pack_user_data(**kwargs):
        name = kwargs.get("name")
        avatar = kwargs.get("avatar")
        gender = kwargs.get("gender")
        wallet = kwargs.get("wallet")
        purchased_amount = kwargs.get("purchased_amount")
        data = {
            "status": Code.success.value,
            "msg": Code.success.name,
            "userName": name,
            "userAvater": avatar,
            "userGender": gender,
            "userWallet": wallet,
            "purchasedAmount": purchased_amount
        }
        return data
