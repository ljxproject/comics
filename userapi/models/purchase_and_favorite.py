from django.db import models

from api.models.self_model import Model


class PurchaseAndFavorite(models.Model, Model):
    PurchaseAndFavoriteStatus_CHOICES = (
        (0, u'购买'),
        (1, u'收藏'),
    )
    email = models.CharField(max_length=64, null=False, verbose_name="用户邮箱")
    com_id = models.IntegerField(null=False, verbose_name="漫画ID")
    status = models.IntegerField(default=0, choices=PurchaseAndFavoriteStatus_CHOICES, verbose_name="当前状态")

    class Meta:
        verbose_name_plural = "用户购买与收藏漫画"
        app_label = "userapi"


    def show_comics_name(self):
        from api.models import Search
        s = Search.get(com_id=self.com_id)
        return s.my_title

    show_comics_name.__name__ = "漫画名"
