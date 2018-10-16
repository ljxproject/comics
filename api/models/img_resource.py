from django.db import models
from django.conf import settings

from api.models.self_model import Model


class ImgResource(models.Model, Model):
    com_id = models.IntegerField(null=False, verbose_name="漫画ID")
    chap_id = models.IntegerField(null=False, verbose_name="章节ID")
    price = models.CharField(max_length=32, default=0.00, verbose_name="章节单价")
    chap_cover_img = models.FilePathField(null=True, blank=True,
                                          path=settings.MEDIA_ROOT + '/%s/%s' % (com_id, chap_id),
                                          verbose_name="章节封面")
    my_title = models.CharField(null=True, max_length=100, verbose_name="章节名称")
    my_img_list_path = models.CharField(null=True, max_length=32, verbose_name="章节图片路径")

    class Meta:
        verbose_name_plural = "漫画内容"
        app_label = "api"

    def show_default_comics_name(self):
        from api.models import Search
        return Search.get(com_id=self.com_id).my_title

    show_default_comics_name.__name__ = "漫画名"
