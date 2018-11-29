from django.db import models

from api.models.self_model import Model


class OrderStatistic(models.Model, Model):
    NAME_CHOICES = (
        (0, u"今日充值"),
        (1, u"昨日充值"),
        (2, u"本月充值"),
        (3, u"本季充值"),
        (4, u"历史充值"),
    )
    name = models.IntegerField(verbose_name="时间", choices=NAME_CHOICES, unique=True)
    income = models.CharField(verbose_name="收入($)", max_length=32)
    paid_order = models.IntegerField(verbose_name="已支付订单数")
    no_paid_order = models.IntegerField(verbose_name="待支付订单数")
    expired_order = models.IntegerField(verbose_name="已失效订单数")
    total_order = models.IntegerField(verbose_name="全部订单数")

    class Meta:
        verbose_name_plural = "简要订单统计"
        app_label = "adminx"
        ordering = ['name']


class OrderStatisticDetail(models.Model, Model):
    date = models.DateField(verbose_name="日期", unique=True)
    income = models.CharField(verbose_name="收入($)", max_length=8)
    expect_income = models.CharField(verbose_name="期望收入($)", max_length=8)
    paid_order = models.IntegerField(verbose_name="已支付订单数")
    no_paid_order = models.IntegerField(verbose_name="待支付订单数")
    expired_order = models.IntegerField(verbose_name="已失效订单数")
    total_order = models.IntegerField(verbose_name="全部订单数")

    class Meta:
        verbose_name_plural = "详细订单统计"
        app_label = "adminx"
