import pickle

from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import r1, r, EnumBase, MyViewBackend, set_attr
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from api.models import ComicInfo, ImgResource
from userapi.models import PurchaseAndFavorite, Permission


class PurchaseChapterViewSet(viewsets.ViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.purchase_chapter(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def purchase_chapter(self, user):
        lang = getattr(self, "lang", "ms")
        system = getattr(self, "app_key")
        email = getattr(self, "email")
        com_id = getattr(self, "comics_id")
        chap_id = getattr(self, "chapter_id")
        com = ComicInfo.get(com_id=com_id)
        chap_id_list_free = [str(i + 1) for i in range(com.free_chapter)]
        if chap_id in chap_id_list_free:
            return EnumBase.get_status(623, CodeEn, lang)  # 该章节免费
        # 该章节是否超出上限
        if int(chap_id) > int(com.total_chapter):
            return EnumBase.get_status(621, CodeEn, lang)  # 该漫画暂无此章节
        # 该用户是否已购买此书
        obj = PurchaseAndFavorite.filter(email=email, com_id=com_id)
        if not obj:
            PurchaseAndFavorite(email=email, com_id=com_id, status=0).save()
        # 调取本章节价格
        i = ImgResource.filter(com_id=com_id, chap_id=chap_id).first()
        price = i.price
        # 扣除价格
        if system == "ios":
            wallet_obj = float(user.wallet_ios)
            wallet = '%.2f' % float(wallet_obj - float(price))
            if wallet >= "0":
                user.wallet_ios = wallet
            else:
                return EnumBase.get_status(635, CodeEn, lang)  # 该用户余额不足
        elif system == "android":
            wallet_obj = float(user.wallet_android)
            wallet = '%.2f' % float(wallet_obj - float(price))
            if wallet >= "0":
                user.wallet_android = wallet
            else:
                return EnumBase.get_status(635, CodeEn, lang)  # 该用户余额不足
        # ttl = r1.ttl(email)
        # r1.set(email, pickle.dumps(user), ttl)
        user.save()
        # 存进redis权限表
        permission_re = ComicMethod.get_user_chapter_authority(email=email, com_id=com_id)
        chap_id_list = eval(permission_re) if isinstance(permission_re, bytes) else permission_re
        # 判断redis是否已有该章节
        if chap_id in chap_id_list:
            return EnumBase.get_status(624, CodeEn, lang)  # 该章节已购
        chap_id_list.append(str(chap_id))
        r.hset("%s_authority" % email, "%s" % com_id, chap_id_list)
        r.expire("%s_authority" % email, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
        Permission.objects.create(com_id=com_id, email=email, chap_id=chap_id)
        com.increase_download()
        return ComicMethod.pack_success_data()
