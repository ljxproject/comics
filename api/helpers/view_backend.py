import pickle

from api.helpers import r1, r, EnumBase
from api.helpers.code import CodeEn
from userapi.models import User


class MyViewBackend(object):
    """
    验证lang email token pin
    """

    # def is_login(self):
    #     # if hasattr(self, "email"):
    #     #     user = r1.get(getattr(self, "email"))
    #     #     if user:
    #     #         return pickle.loads(user)
    #     # todo
    #     if hasattr(self, "email"):
    #         user = User.get(getattr(self, "email"))
    #         if user:
    #             return user
    #     return False

    def is_valid_lang(self):
        return True if getattr(self, "lang", "ms") in eval(r.get("lang")) else False

    def is_valid_email(self):
        if hasattr(self, "email") and User.filter(email=getattr(self, "email").lower()):
            return True
        return False

    def is_valid_token(self):
        # if hasattr(self, "token"):
        #     user = self.is_login()
        #     if user and getattr(self, "token") == user.token:
        #         return user
        # todo
        if hasattr(self, "token") and hasattr(self, "email") and r1.get(getattr(self, "email")):
            if eval(r1.get(getattr(self, "email")))["token"] == getattr(self, "token"):
                return True
        return False

    def is_valid_pin(self):
        """
        :return: valid pin return True, else False
        """
        redis_pin = r1.get("%s_PIN" % getattr(self, "email"))
        if redis_pin and str(eval(redis_pin)) == str(getattr(self, "pin")):
            return True
        return False

    def is_exist_email(self, email):
        """
        :return: exist email return False, else True
        """
        if User.filter(email=email).exists():
            return False
        return True

    def _pre_check(self):
        if not self.is_valid_lang():
            return EnumBase.get_status(642, CodeEn)  # 暂无此语言
        lang = getattr(self, "lang", "ms")
        if not self.is_valid_token():
            return EnumBase.get_status(634, CodeEn, lang)  # 该用户并未登录
        if not self.is_valid_email():
            return EnumBase.get_status(639, CodeEn, lang)  # 该用户邮箱信息有误
        return User.get(email=getattr(self, "email").lower())
