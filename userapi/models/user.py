from django.db import models

from api.models.self_model import Model


class User(models.Model, Model):
    GENDER_CHOICES = (
        (0, u'男'),
        (1, u'女'),)
    SYSTEM_CHOICES = (
        (0, u'ios'),
        (1, u'android'),
    )
    email = models.CharField(unique=True, max_length=64, null=False, verbose_name="用户邮箱")
    name = models.CharField(null=True, blank=True, max_length=10, verbose_name="昵称")
    avatar = models.ImageField(blank=True, null=True, upload_to="uploads/avatar", verbose_name="头像")
    gender = models.IntegerField(blank=True, null=True, choices=GENDER_CHOICES, verbose_name="性别")
    wallet_ios = models.CharField(max_length=32, default="0.00", verbose_name="钱包(ios)")
    wallet_android = models.CharField(max_length=32, default="0.00", verbose_name="钱包(android)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_online = models.DateTimeField(auto_now=True, verbose_name="上次登录时间")
    login_lock = models.BooleanField(default=False, verbose_name="登录锁")
    bind = models.CharField(max_length=100, blank=True, null=True, verbose_name="第三方绑定ID")
    active = models.BooleanField(default=0, verbose_name="是否在线")
    accumulative_time = models.IntegerField(default=0, verbose_name="累计登录时长（小时）")

    class Meta:
        verbose_name_plural = "用户"
        app_label = "userapi"

    def show_accumulative_time(self):
        return "%.2f" % (self.accumulative_time / 3600)
    show_accumulative_time.__name__ = "累计登录时长（小时）"