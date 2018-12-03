from django.db import models

from api.models.self_model import Model


class Transaction(models.Model, Model):
    TransactionStatus_CHOICES = (
        (0, u'待支付'),
        (1, u'已支付'),
        (2, u'已过期'),
    )
    tx_id = models.CharField(unique=True, max_length=128, null=False, verbose_name="交易ID")
    email = models.CharField(max_length=64, null=False, verbose_name="用户邮箱")
    platform = models.CharField(max_length=64, null=False, verbose_name="充值渠道")
    gmv = models.CharField(max_length=32, null=False, verbose_name="交易金额($)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pay_time = models.DateTimeField(null=True, default=None, verbose_name="支付时间")
    status = models.IntegerField(default=0, choices=TransactionStatus_CHOICES, verbose_name="当前支付状态")
    receipt_id = models.BigIntegerField(null=True, blank=True, verbose_name="第三方交易凭证ID")

    class Meta:
        verbose_name_plural = "交易记录"
        app_label = "userapi"
