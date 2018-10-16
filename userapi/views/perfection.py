import os

from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from PIL import Image

from userapi.models import Transaction
from api.helpers.code import Code
from api.helpers.comic_method import ComicMethod
from api.helpers.make_order import make_order
from api.helpers.serializer import ComicsSuccessSerializer, UsersGenderSerializer, UsersEmailSerializer, \
    UsersNameSerializer, UsersWalletSerializer, UsersAvaterSerializer, CreateOderSerializer

from userapi.models import User
from api.helpers import img_handler, r1
from userapi.pay_task import user_lock_release, order_expires

import logging

logger = logging.getLogger('comics.app')


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()


class ChangeEmailViewSet(viewsets.ModelViewSet):
    serializer_class = UsersEmailSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = UsersEmailSerializer(data=request.data)
        if form.is_valid():
            old_email = form.data.get("oldEmail")
            new_email = form.data.get("newEmail")
            pin = form.data.get("pin")
            # 验证email
            if (pin != str(eval(r1.get("%s_PIN" % old_email)))) or (not r1.get("%s_PIN" % old_email)):
                data = {
                    "status": Code.captcha_not_match.value,
                    "msg": Code.captcha_not_match.name.replace("_", " ").title(),
                }
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            else:
                if User.filter(email=new_email):
                    data = {
                        "status": Code.user_existed.value,
                        "msg": Code.user_existed.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                user = User.get(email=old_email)
                user.email = new_email
                # 修改图片名
                old_img = str(user.avatar)
                suffix = os.path.splitext(old_img)[1]
                path = os.path.join(settings.MEDIA_ROOT, "avatar")
                os.rename(os.path.join(path, old_img), os.path.join(path, str(new_email) + suffix))
                user.avatar = str(new_email) + suffix
                user.save()
                data = ComicMethod.pack_success_data()
        else:
            data = {
                "status": Code.modify_failed.value,
                "msg": Code.modify_failed.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


class ChangeGenderViewSet(viewsets.ModelViewSet):
    serializer_class = UsersGenderSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = UsersGenderSerializer(data=request.data)
        if form.is_valid():
            email = form.data.get("email")
            gender = form.data.get("gender")
            user = User.get(email=email)
            user.gender = gender
            user.save()
            data = ComicMethod.pack_success_data()
        else:
            data = {
                "status": Code.modify_failed.value,
                "msg": Code.modify_failed.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


class ChangeAvatarViewSet(viewsets.ModelViewSet):
    serializer_class = UsersAvaterSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = UsersAvaterSerializer(data=request.data)
        if form.is_valid():
            email = form.validated_data.get("email")
            img = form.validated_data.get("avatar")
            user = User.get(email=email)
            filename = img.name
            re = img_handler.avatar_handler(filename)
            if isinstance(re, dict):
                data = re
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            avatar = Image.open(img)
            if avatar:
                old_filename = str(user.avatar)
            else:
                old_filename = ""
            filename = re
            if old_filename:
                old_pathname = os.path.join(settings.MEDIA_ROOT, "uploads/avatar", old_filename)
                if os.path.exists(old_pathname):
                    os.remove(old_pathname)
            pathname = os.path.join(settings.MEDIA_ROOT, "uploads/avatar", filename)
            avatar.save(pathname)
            user.avatar = filename
            user.save()
            data = ComicMethod.pack_success_data()
        else:
            data = {
                "status": Code.modify_failed.value,
                "msg": Code.modify_failed.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


class ChangeNameViewSet(viewsets.ModelViewSet):
    serializer_class = UsersNameSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = UsersNameSerializer(data=request.data)
        if form.is_valid():
            email = form.data.get("email")
            name = form.data.get("name")
            user = User.get(email=email)
            user.name = name
            user.save()
            data = ComicMethod.pack_success_data()
        else:
            data = {
                "status": Code.modify_failed.value,
                "msg": Code.modify_failed.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


class ChangeWalletViewSet(viewsets.ModelViewSet):
    serializer_class = UsersWalletSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = UsersWalletSerializer(data=request.data)
        if form.is_valid():
            tx_id = form.data.get("txID")
            system = request.data.get("system")
            t = Transaction.get(tx_id=tx_id)
            email = t.email
            gmv = t.gmv
            user = User.get(email=email)
            if system == "ios":
                wallet_obj = float(user.wallet_ios)
                wallet = str(wallet_obj + float(gmv))
                user.wallet_ios = wallet
            elif system == "android":
                wallet_obj = float(user.wallet_android)
                wallet = str(wallet_obj + float(gmv))
                user.wallet_android = wallet
            user.login_lock = False
            user.save()
            t.pay_time = timezone.now()
            t.status = 1
            t.save()
            data = ComicMethod.pack_success_data()
        else:
            data = {
                "status": Code.modify_failed.value,
                "msg": Code.modify_failed.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


class CreateOderViewSet(viewsets.ModelViewSet):
    serializer_class = CreateOderSerializer

    # throttle_classes = [OrderRateThrottle, ]

    # def get(self, request, *args, **kwargs):
    #     self.dispatch
    #     return Response('控制访问频率示例')

    # def throttled(self, request, wait):
    #
    #     class MyThrottled(exceptions.Throttled):
    #         default_detail = '请求被限制.'
    #         extra_detail_singular = 'Expected available in {wait} second.'
    #         extra_detail_plural = '还需要再等待{wait}'
    #
    #     raise MyThrottled(wait)

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        form = CreateOderSerializer(data=request.data)
        if form.is_valid():
            email = form.data.get("email")
            gmv = form.data.get("gmv")
            platform = form.data.get("platform")
            tx_id = make_order()
            t = Transaction(tx_id=tx_id, email=email, gmv=gmv, platform=platform)
            t.save()
            order_expires.apply_async(args=(tx_id,), countdown=7 * 24 * 60 * 60)  # todo 7*24*60*60
            u = User.get(email=email)
            u.login_lock = 1
            u.save()
            user_lock_release.apply_async(args=(email,), countdown=5 * 60)  # todo 5*60
            data = ComicMethod.pack_success_data(tx_id=tx_id)
        else:
            data = {
                "status": Code.unknown_error.value,
                "msg": Code.unknown_error.name.replace("_", " ").title(),
            }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
