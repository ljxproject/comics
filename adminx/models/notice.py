from django.db import models

from api.models.self_model import Model


class Notice(models.Model, Model):
    name = models.CharField(max_length=64, verbose_name="公告名")
    file = models.FileField(null=False, upload_to="uploads/notices", verbose_name="公告文档")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "公告信息"
        app_label = "adminx"
