from django.db import models

from api.models.self_model import Model


class MangaUpload(models.Model, Model):
    name = models.CharField(max_length=64, verbose_name="文件名 ")
    resources_file = models.CharField(max_length=128, verbose_name="资源路径")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "漫画上传"
        app_label = "adminx"
