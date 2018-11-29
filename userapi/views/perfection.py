import os
import pickle

from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from PIL import Image

from userapi.models import FeedBack, PurchaseAndFavorite, Permission, Transaction, User
from api.helpers import EnumBase, r1, MyViewBackend, set_attr, img_handler, r
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.make_order import make_order
from api.helpers.serializer import ComicsSuccessSerializer
from userapi.pay_task import user_lock_release, order_expires, logout

import logging

logger = logging.getLogger('comics.app')


class ChangeEmailViewSet(viewsets.ModelViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.email_update(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def email_update(self, user):
        """
        update user email
        :return: API data
        """
        new_email = getattr(self, "value").lower()
        lang = getattr(self, "lang", "ms")
        if not self.is_valid_pin():
            return EnumBase.get_status(638, CodeEn, lang)  # 该用户验证失败
        if r1.get(new_email):
            return EnumBase.get_status(632, CodeEn, lang)  # 该用户已存在
        try:
            obj_list = [FeedBack, PurchaseAndFavorite, Transaction]

            # 从redis中获取旧email
            old_email = user.email
            # 处理图片名字
            old_img = str(user.avatar)
            suffix = os.path.splitext(old_img)[1]
            path = os.path.join(settings.MEDIA_ROOT, "avatar")
            if os.path.exists(os.path.join(path, old_img)):
                os.rename(os.path.join(path, old_img), os.path.join(path, str(new_email) + suffix))
                # 修改redis中avatar的名字
                user.avatar = str(new_email) + suffix
            # 修改redis中email
            user.email = new_email
            # 修改feedback, PurchaseAndFavorite,Transaction中email
            for o in obj_list:
                o.filter(email=old_email).update(email=new_email)
            # 更改redis permission
            r.rename(old_email + "_authority", new_email + "_authority")
            # # 获取redis旧email的存活时间
            # ttl = r1.ttl(old_email)
            # # 设置logout时间 ttl-3600s
            # logout_ttl = ttl - 3600
            # # 删除redis旧email
            # r1.delete(old_email)
            # # 重新往redis插入以新email为键名的user对象
            # r1.setex(new_email, pickle.dumps(user), ttl)
            # # 重新设置logout过期任务
            # logout.apply_async(args=(new_email,), countdown=logout_ttl)

            user.save()
            r1.delete(getattr(self, "token"))

        except :
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败

        else:
            return ComicMethod.pack_success_data()  # todo 要求重新登录


class ChangeGenderViewSet(viewsets.ModelViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.gender_update(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def gender_update(self, user):
        lang = getattr(self, "lang", "ms")
        gender = getattr(self, "value")
        try:
            # setattr(user, "gender", gender)
            # ttl = r1.ttl(email)
            # r1.setex(email, pickle.dumps(user), ttl)
            user.gender = gender
            user.save()
        except:
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败
        else:
            return ComicMethod.pack_success_data()


class ChangeAvatarViewSet(viewsets.ModelViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.avatar_update(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def avatar_update(self, user):
        """
        update user avatar
        :return: API data
        """
        avatar = getattr(self, "avatar")
        lang = getattr(self, "lang", "ms")
        try:
            filename = avatar.name
            re = img_handler.avatar_handler(filename)
            if isinstance(re, Exception):
                return EnumBase.get_status(641, CodeEn, lang)  # 图片不合法
            avatar = Image.open(avatar)
            if avatar:
                old_filename = str(user.avatar)
            else:
                old_filename = ""
            new_filename = re
            if old_filename:
                old_pathname = os.path.join(settings.MEDIA_ROOT, "uploads/avatar", old_filename)
                if os.path.exists(old_pathname):
                    os.remove(old_pathname)
            pathname = os.path.join(settings.MEDIA_ROOT, "uploads/avatar", new_filename)
            avatar.save(pathname)
            user.avatar = new_filename
            # ttl = r1.ttl(email)
            # r1.setex(email, pickle.dumps(user), ttl)
            user.save()
        except:
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败
        else:
            return ComicMethod.pack_success_data()


class ChangeNameViewSet(viewsets.ModelViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.name_update(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def name_update(self, user):
        lang = getattr(self, "lang", "ms")
        name = getattr(self, "value")
        try:
            # setattr(user, "name", name)
            # ttl = r1.ttl(email)
            # r1.setex(email, pickle.dumps(user), ttl)
            user.name = name
            user.save()
        except:
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败
        else:
            return ComicMethod.pack_success_data()


class ChangeWalletViewSet(viewsets.ViewSet, MyViewBackend):

    @set_attr
    def post(self, request):
        data = self.wallet_update()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def wallet_update(self):
        tx_id = getattr(self, "tx_id")
        lang = getattr(self, "lang", "ms")
        try:
            t = Transaction.get(tx_id=tx_id)
            if t.status != 0:
                return EnumBase.get_status(660, CodeEn, lang)
            email = t.email
            gmv = t.gmv
            platform = t.platform
            setattr(self, "email", email)
            data = self._pre_check()
            if isinstance(data, dict):
                # user = pickle.loads(r1.get(email))
                # ttl = r1.ttl(email)
                # user.login_lock = 0
                # r1.set(email, pickle.dumps(user), ttl)
                User.filter(email=email).update(login_lock=0)
                return data
            user = data
            if platform == "ios":
                wallet_obj = float(user.wallet_ios)
                wallet = '%.2f' % (wallet_obj + float(gmv))
                user.wallet_ios = wallet
            elif platform == "android":
                wallet_obj = float(user.wallet_android)
                wallet = '%.2f' % (wallet_obj + float(gmv))
                user.wallet_android = wallet
            # ttl = r1.ttl(email)
            user.login_lock = 0
            user.save()
            # r1.set(email, pickle.dumps(user), ttl)
            t.pay_time = timezone.now()
            t.status = 1
            t.save()
        except:
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败
        else:
            return ComicMethod.pack_success_data()


class CreateOderViewSet(viewsets.ModelViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.create_order(data)
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def create_order(self, user):
        lang = getattr(self, "lang", "ms")
        gmv = getattr(self, "gmv")
        platform = getattr(self, "app_key")
        email = getattr(self, "email")
        try:
            tx_id = make_order()
            t = Transaction(tx_id=tx_id, email=email, gmv=gmv, platform=platform)
            t.save()
            order_expires.apply_async(args=(tx_id,), countdown=7 * 24 * 60 * 60)  # todo 7*24*60*60
            # ttl = r1.ttl(email)
            user.login_lock = 1
            # r1.set(email, pickle.dumps(user), ttl)
            user.save()
            user_lock_release.apply_async(args=(email,), countdown=60)  # todo 60
        except:
            return EnumBase.get_status(636, CodeEn, lang)  # 该用户信息更改失败
        else:
            return ComicMethod.pack_success_data(tx_id=tx_id)
