from django.db import models

from api.models.self_model import Model
from api.helpers.code import Code


class Search(models.Model, Model):
    com_id = models.IntegerField(unique=True, verbose_name="漫画ID")

    """马来语my"""
    my_title = models.CharField(null=True, max_length=100, verbose_name="漫画名")
    my_author = models.CharField(null=True, max_length=100, verbose_name="漫画作者")
    my_subtitle = models.TextField(null=True, verbose_name="漫画副标题")
    my_introduction = models.TextField(null=True, verbose_name="漫画简介")

    class Meta:
        verbose_name_plural = "漫画检索"
        app_label = "api"


