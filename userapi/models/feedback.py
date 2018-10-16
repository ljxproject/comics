from django.db import models

from api.models.self_model import Model


class FeedBack(models.Model, Model):
    FeedBackStatus_CHOICES = (
        (0, u'待处理'),
        (1, u'已处理'),
    )
    email = models.CharField(max_length=64, null=False, verbose_name="用户邮箱")
    award = models.CharField(max_length=32, default="0.00", verbose_name="奖励金额")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified = models.DateTimeField(auto_now=True, verbose_name="最后编辑时间")
    status = models.IntegerField(default=0, choices=FeedBackStatus_CHOICES, verbose_name="漫画当前状态")
    fbd_id = models.IntegerField(unique=True, verbose_name="意见反馈详情ID")

    class Meta:
        verbose_name_plural = "意见反馈"
        app_label = "userapi"


class FeedBackDetail(models.Model, Model):
    email = models.CharField(max_length=64, null=False, verbose_name="用户邮箱")
    title = models.CharField(max_length=100, verbose_name="意见主题")
    system = models.CharField(blank=True, null=True, max_length=16, verbose_name='操作系统')
    content = models.TextField(verbose_name="意见内容")
    picture = models.FileField(upload_to="uploads/feedback", blank=True, null=True,
                               verbose_name="截图")

    class Meta:
        verbose_name_plural = "意见详细信息"
        app_label = "userapi"
