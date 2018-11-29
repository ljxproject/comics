import pickle
import hashlib
import time

from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import r1, EnumBase, MyViewBackend, set_attr
from api.helpers.code import CodeEn
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from userapi.sms_task import send_email
from userapi.pay_task import logout
from userapi.models import User


class UsersLogin(viewsets.ViewSet, MyViewBackend):
    """
    define user login logout register interfaces
    """

    def get_qs(self, model, perm_dict):
        """
        :param model:
        :param perm_dict: filter perms
        :return: queryset obj
        """
        return model.filter(**perm_dict)

    @set_attr
    def post(self, request):
        """
        execute different function by the request key of behavior
        behavior including send_code, login, and logout.
        :param request:
        :return: API data
        """
        if self.is_valid_lang():
            data = self.login()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def _register(self, bind_id=None):
        """
        register
        :return: success register return user object, else API data
        """
        lang = getattr(self, "lang", "ms")
        if hasattr(self, "email") and hasattr(self, "pin"):
            email = getattr(self, "email")
            if not self.is_valid_pin():
                data = EnumBase.get_status(638, CodeEn, lang)  # 该用户验证失败
                return data
            elif not self.is_exist_email(email):
                return EnumBase.get_status(632, CodeEn, lang)  # 该用户已存在
            else:
                user = User(email=email, wallet_ios="5.00", wallet_android="5.00", bind=bind_id,
                            active=1, accumulative_time=0)
                user.save()
                return user
        else:
            data = EnumBase.get_status(639, CodeEn, lang)  # 该用户邮箱信息有误
            return data

    def has_login_lock(self, obj):
        """
        :param obj:
        :return: have lock return API data, else user obj
        """
        # email = obj.email
        # # redis取，没有mysql取
        # redis_obj = r1.get(email)
        lang = getattr(self, "lang", "ms")
        #
        # if redis_obj:
        #     obj = pickle.loads(redis_obj)
        if obj.login_lock == 1:
            return EnumBase.get_status(637, CodeEn, lang)  # 该用户注册登录失败
        return obj

    def qs_has_obj(self, qs, bind_id=None):
        """
        :param queryset:
        :return: success register or querset have obj return user obj, else API data
        """
        if not qs:
            return self._register(bind_id)
        else:
            # 验证已有用户登录锁是否激活
            data = self.has_login_lock(qs.first())
            return data

    def login(self):
        """
        execute login and register function
        :return: API data
        """
        # 获取bind——id
        # 有bind——id
        lang = getattr(self, "lang", "ms")
        if hasattr(self, "bind_id"):
            bind_id = getattr(self, "bind_id")
            # 根据bind——id 获取user对象，对象存在且则登录
            qs = self.get_qs(User, {"bind": bind_id})
            # 无user对象则 取email pin 注册
            data = self.qs_has_obj(qs, bind_id)
            if isinstance(data, dict):
                return data
            else:
                user = data
        # 无bind-id 取email pin 根据email取对象 存在则登录
        else:
            # if not self.is_valid_email():
            #     print("LO")
            #     return EnumBase.get_status(639, CodeEn, lang)  # 该用户邮箱信息有误

            email = getattr(self, "email")

            if not self.is_valid_pin():
                data = EnumBase.get_status(638, CodeEn, lang)  # 该用户验证失败
                return data
            qs = self.get_qs(User, {"email": email})
            # 无user对象则注册
            data = self.qs_has_obj(qs)
            if isinstance(data, dict):
                return data
            else:
                user = data

        # 登录操作
        user.active = 1
        user.save()
        email = user.email
        timestamp = "%.f" % time.time()
        key = email + settings.SECRET_KEY + timestamp
        # 生成token，email+key+time md5加密
        token = hashlib.md5(key.encode("utf-8")).hexdigest()
        #
        # if not hasattr(user, "timestamp"):
        #     user.timestamp = timestamp
        # # 往user对象存token
        # user.token = token
        # # 把对象存进redis
        # r1.setex(email, pickle.dumps(user), 2 * 7 * 25 * 60 * 60)  # 活跃时间 2 * 7 * 24 * 60 * 60(两周)
        # logout.apply_async(args=(user.email,),
        #                    countdown=2 * 7 * 24 * 60 * 60)  # todo 活跃时间 2 * 7 * 24 * 60 * 60(两周)
        # todo
        r1.setex(email, {"timestamp": timestamp, "token": token}, 2 * 7 * 25 * 60 * 60)
        logout.apply_async(args=(email,), countdown=2 * 7 * 25 * 60 * 60)
        return ComicMethod.pack_success_data(token=token, email=email)


class UsersSendCode(viewsets.ViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        if self.is_valid_lang():
            data = self.send_code()
        else:
            data = EnumBase.get_status(642, CodeEn)  # 暂无此语言
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def send_code(self):
        """
        send pin code
        :return: API data
        """
        email = getattr(self, "email")
        template = getattr(self, "template")
        lang = getattr(self, 'lang', "ms")
        send_email.delay(email, template, lang)
        return ComicMethod.pack_success_data()


class UsersLogout(viewsets.ViewSet, MyViewBackend):
    @set_attr
    def post(self, request):
        data = self._pre_check()
        if not isinstance(data, dict):
            data = self.logout()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def logout(self):
        """
        user logout
        :return: API data
        """
        # email = getattr(self, "email")
        # logout.delay(email)
        # todo
        email = getattr(self, "email")
        logout.delay(email)
        return ComicMethod.pack_success_data()
