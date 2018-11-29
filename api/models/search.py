from django.db import models

from api.models.self_model import Model


class Search(models.Model, Model):
    com_id = models.IntegerField(unique=True, verbose_name="漫画ID")

    """英语en"""
    en_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画名(en)")
    en_author = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画作者(en)")
    en_subtitle = models.TextField(null=True, blank=True, verbose_name="漫画副标题(en)")
    en_introduction = models.TextField(null=True, blank=True, verbose_name="漫画简介(en)")

    """越南语vi"""
    vi_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画名(vi)")
    vi_author = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画作者(vi)")
    vi_subtitle = models.TextField(null=True, blank=True, verbose_name="漫画副标题(vi)")
    vi_introduction = models.TextField(null=True, blank=True, verbose_name="漫画简介(vi)")

    """马来语ms"""
    ms_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画名(ms)")
    ms_author = models.CharField(null=True, blank=True, max_length=100, verbose_name="漫画作者(ms)")
    ms_subtitle = models.TextField(null=True, blank=True, verbose_name="漫画副标题(ms)")
    ms_introduction = models.TextField(null=True, blank=True, verbose_name="漫画简介(ms)")

    class Meta:
        verbose_name_plural = "漫画检索"
        app_label = "api"
