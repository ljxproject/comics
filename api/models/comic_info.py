import os

from django.db import models
from django.conf import settings

from enum import Enum, unique

from api.helpers import EnumBase
from api.helpers.code import ComicEn, ComicZh, CategoryEn, CategoryZh
from api.models.self_model import Model


# @unique
# class ComicStatus(Enum):
#     """空"""
#     none = 0
#     """已完结"""
#     finish = 1001
#     """连载中"""
#     serial = 1002
#     """免费"""
#     free = 1003
#
#     @staticmethod
#     def get_name_from_value(num):
#         for i in ComicStatus.__members__.values():
#             if i.value == num:
#                 return i.name


class ComicInfo(models.Model, Model):
    RECOMMEND = (
        (0, "其他分类"),
        (1, "主编推荐"),
        (2, "完结推荐"),
        (3, "热门推荐"),
    )
    CATEGORY_STATUS = EnumBase.get_model_status(CategoryEn, CategoryZh)

    COMIC_STATUS = EnumBase.get_model_status(ComicEn, ComicZh)
    com_id = models.IntegerField(unique=True, null=False, verbose_name="漫画ID")
    # my_com_cover_img = models.FilePathField(null=True, blank=True, path=settings.MEDIA_ROOT + '/%s' % com_id,
    #                                         verbose_name="漫画封面(my)")
    # vn_com_cover_img = models.FilePathField(null=True, blank=True, path=settings.MEDIA_ROOT + '/%s' % com_id,
    #                                         verbose_name="漫画封面(vn)")

    free_chapter = models.IntegerField(default=0, verbose_name="免费章节数")
    total_chapter = models.IntegerField(default=0, verbose_name="已有章节数")
    download = models.BigIntegerField(default=0, verbose_name="下载量")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    status = models.IntegerField(default=1002, choices=COMIC_STATUS, verbose_name="漫画当前状态")
    category = models.IntegerField(default=0, choices=CATEGORY_STATUS, verbose_name="漫画当前分类")

    # recommend = models.IntegerField(default=0, choices=RECOMMEND, verbose_name="漫画当前推荐")

    # 增加计算漫画下载量
    def increase_download(self):
        # 每次调用此方法，就把download加1
        self.download += 1
        # 只更新download字段
        self.save(update_fields=['download'])

    class Meta:
        verbose_name_plural = "漫画信息"
        app_label = "api"

    def show_default_comics_name(self):
        from api.models import Search
        title = Search.get(com_id=self.com_id).en_title
        return title if title else "空"

    show_default_comics_name.__name__ = "漫画名"

    # def change_status(self):
    #     s_k = [i for i in ComicStatus.__members__.keys()]
    #     s_v = [i.value for i in ComicStatus.__members__.values()]
    #     s = dict(zip(s_v, s_k))
    #     if self.status in s_v:
    #         return s[self.status]
    #
    # change_status.__name__ = "漫画当前状态"

    # def change_category(self):
    #     from api.models import CategoryStatus
    #     c_k = [i for i in CategoryStatus.__members__.keys()]
    #     c_v = [i.value for i in CategoryStatus.__members__.values()]
    #     c = dict(zip(c_v, c_k))
    #     if self.category in c_v:
    #         return c[self.category]
    #
    # change_category.__name__ = "漫画当前分类"


class ComicCoverImg(models.Model, Model):
    com_id = models.IntegerField(unique=True, null=False, verbose_name="漫画ID")
    vi_comic_cover_img = models.FilePathField(null=True, blank=True,
                                              path=os.path.join(settings.MEDIA_ROOT, "img", '%s' % com_id),
                                              verbose_name="漫画封面(vi)")
    en_comic_cover_img = models.FilePathField(null=True, blank=True,
                                              path=os.path.join(settings.MEDIA_ROOT, "img", '%s' % com_id),
                                              verbose_name="漫画封面(en)")
    ms_comic_cover_img = models.FilePathField(null=True, blank=True,
                                              path=os.path.join(settings.MEDIA_ROOT, "img", '%s' % com_id),
                                              verbose_name="漫画封面(ms)")
