from django.db import models

from api.models.self_model import Model


class DataBackup(models.Model, Model):
    BACKUP_TYPE_CHOICES = (
        (0, u'完全备份'),
        (1, u'差异备份'),
        (2, u'增量备份'),
    )
    name = models.CharField(max_length=64, unique=True, verbose_name="备份文件名")
    backup_type = models.IntegerField(choices=BACKUP_TYPE_CHOICES, verbose_name="备份类型")
    backup_file = models.CharField(max_length=128, verbose_name="备份文件路径")
    size = models.CharField(max_length=16, verbose_name="备份文件大小")
    comment = models.TextField(verbose_name="备注", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    base = models.IntegerField(null=True, blank=True, verbose_name='父备份ID')

    class Meta:
        verbose_name_plural = "备份"
        app_label = "adminx"
