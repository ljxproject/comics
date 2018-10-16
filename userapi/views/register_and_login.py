import random

from django.conf import settings
from redis_sessions.session import SessionStore
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers.code import Code
from api.helpers.serializer import ComicsSuccessSerializer
from api.helpers.comic_method import ComicMethod
from api.helpers import r1

from userapi.models import User
from userapi.pay_task import active_to_inactive
from userapi.sms_task import send_email


@api_view(["POST"])
def register_and_login(request):
    """
    用户注册与登录
    接收 email PIN
    """
    # 验证表单是否合法
    if request.method == 'POST':
        email = request.data.get("email")
        pin = request.data.get("PIN")
        bind_id = request.data.get("bindID")

        # 是否第三方登录
        if bind_id:
            # 验证此第三方id是否已有账号
            u = User.filter(bind=bind_id)
            if len(u) == 0:
                if not email:
                    data = {
                        "status": Code.email_error.value,
                        "msg": Code.email_error.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                if not (r1.get("%s_PIN" % email)) or (str(pin) != str(eval(r1.get("%s_PIN" % email)))):
                    data = {
                        "status": Code.captcha_not_match.value,
                        "msg": Code.captcha_not_match.name.replace("_", " ").title(),
                    }
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
                eu = User.filter(email=email)
                if eu:
                    if eu[0].bind:
                        data = {
                            "status": Code.this_email_has_been_bound.value,
                            "msg": Code.this_email_has_been_bound.name.replace("_", " ").title(),
                        }
                        serializer = ComicsSuccessSerializer(data)
                        return Response(serializer.data)
                    eu[0].bind = bind_id
                    eu[0].save()
                # 不存在则注册
                else:
                    user = User(email=email, wallet_ios="10.00", wallet_android="10.00", bind=bind_id, active=1)
                    user.save()
            else:
                email = u[0].email
        # 非第三方登录
        else:
            # 验证验证码
            if not (r1.get("%s_PIN" % email)) or (str(pin) != str(eval(r1.get("%s_PIN" % email)))):
                data = {
                    "status": Code.captcha_not_match.value,
                    "msg": Code.captcha_not_match.name.replace("_", " ").title(),
                }
                serializer = ComicsSuccessSerializer(data)
                return Response(serializer.data)
            # 判断email是否存在
            u = User.filter(email=email)
            if not u:
                # 不存在则注册
                user = User(email=email, wallet_ios="10.00", wallet_android="10.00", active=1)
                user.save()
        # 验证锁
        if u and u[0].login_lock:
            data = {
                "status": Code.sign_in_failed.value,
                "msg": Code.sign_in_failed.name.replace("_", " ").title(),
            }
            serializer = ComicsSuccessSerializer(data)
            return Response(serializer.data)
        # 登录
        u[0].active = 1
        u[0].save()
        active_to_inactive.apply_async(args=(u[0],),
                                       countdown=2 * 7 * 24 * 60 * 60)  # todo 活跃时间 2 * 7 * 24 * 60 * 60(两周)
        sessionstore = SessionStore()
        sessionstore[email] = email + settings.SECRET_KEY + str(random.randint(0, 10))
        sessionstore.save()
        if r1.get(email):
            old_key = r1.get(email)
            r1.delete(old_key)
        r1.set(email, sessionstore.session_key)
        data = ComicMethod.pack_success_data(email=email)
        serializer = ComicsSuccessSerializer(data)
        response = Response(serializer.data)
        response.set_cookie(
            settings.SESSION_COOKIE_NAME,
            sessionstore.session_key,
            domain=settings.SESSION_COOKIE_DOMAIN,
            path=settings.SESSION_COOKIE_PATH,
            secure=settings.SESSION_COOKIE_SECURE or None,
            httponly=settings.SESSION_COOKIE_HTTPONLY or None,
        )
        return response
    else:
        data = {
            "status": Code.sign_in_failed.value,
            "msg": Code.sign_in_failed.name.replace("_", " ").title(),
        }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


@api_view(["POST"])
def logout(request):
    """
    用户注销
    接收email
    """
    # 删除session
    try:
        email = str(request.data.get("email"))
        u = User.get(email=email)
        u.active = 0
        u.save()
        del request.session[email]
        data = ComicMethod.pack_success_data()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    except:
        data = {
            "status": Code.unknown_error.value,
            "msg": Code.unknown_error.name.replace("_", " ").title()
        }
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)


@api_view(["POST"])
def send_code(request):
    if request.method == 'POST':
        email = request.data.get("email")
        template = request.data.get("template")
        send_email.delay(email, template)
        data = ComicMethod.pack_success_data()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)
    else:
        return Response(request.data)


@api_view(["GET"])
def check_session(request):
    email = request.GET.get("email")
    value = request.session.get(email)
    if value:
        data = ComicMethod.pack_success_data()
    else:
        data = {
            "status": Code.you_are_offline_in_this_device.value,
            "msg": Code.you_are_offline_in_this_device.name.replace("_", " ").title(),
        }
    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
