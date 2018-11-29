from django.db import models
from django.conf import settings

from api.models.self_model import Model


class ImgResource(models.Model, Model):
    com_id = models.IntegerField(verbose_name="漫画ID")
    chap_id = models.IntegerField(verbose_name="章节ID")
    price = models.CharField(max_length=32, default=0.00, verbose_name="章节单价")
    chap_cover_img = models.FilePathField(null=True, blank=True,
                                          path=settings.MEDIA_ROOT + '/%s/%s' % (com_id, chap_id),
                                          verbose_name="章节封面")
    en_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="章节名称(en)")
    en_img_list_path = models.CharField(null=True, blank=True, max_length=32, verbose_name="章节图片路径(en)")
    #
    vi_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="章节名称(vi)")
    vi_img_list_path = models.CharField(null=True, blank=True, max_length=32, verbose_name="章节图片路径(vi)")

    ms_title = models.CharField(null=True, blank=True, max_length=100, verbose_name="章节名称(ms)")
    ms_img_list_path = models.CharField(null=True, blank=True, max_length=32, verbose_name="章节图片路径(ms)")

    class Meta:
        verbose_name_plural = "漫画内容"
        app_label = "api"

    def show_default_comics_name(self):
        from api.models import Search
        title = Search.get(com_id=self.com_id).en_title
        return title if title else "空"

    show_default_comics_name.__name__ = "漫画名"

# class ChapterCoverImg(models.Model, Model):
#     com_id = models.IntegerField(verbose_name="漫画ID")
#     chap_id = models.IntegerField(verbose_name="章节ID")
#     vi_chap_cover_img = models.FilePathField(null=True, blank=True,
#                                              path=settings.MEDIA_ROOT + '/%s/%s' % (com_id, chap_id),
#                                              verbose_name="章节封面(vi)")
#     en_chap_cover_img = models.FilePathField(null=True, blank=True,
#                                              path=settings.MEDIA_ROOT + '/%s/%s' % (com_id, chap_id),
#                                              verbose_name="章节封面(en)")


# class ChapterTitle(models.Model, Model):
#     com_id = models.IntegerField(verbose_name="漫画ID")
#     chap_id = models.IntegerField(verbose_name="章节ID")
#     vi_title = models.CharField(null=True, max_length=100, verbose_name="章节名称(vi)")
#     en_title = models.CharField(null=True, max_length=100, verbose_name="章节名称(en)")


# class ChapterImgPath(models.Model, Model):
#     vi_img_list_path = models.CharField(null=True, max_length=32, verbose_name="章节图片路径(vi)")
#     en_img_list_path = models.CharField(null=True, max_length=32, verbose_name="章节图片路径(en)")
