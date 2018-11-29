from django.db import models
from enum import Enum, unique
from api.helpers import EnumBase
from api.helpers.code import CategoryZh, CategoryEn

from api.models.self_model import Model


# @unique
# class CategoryStatus(Enum):
#     """主编推荐"""
#     editor_recommend = 1
#     """完结推荐"""
#     finish_recommend = 2
#     """热门推荐"""
#     trend_recommend = 3
#     """中漫"""
#     manhua = 10
#     """日漫"""
#     manga = 11
#
#     @staticmethod
#     def to_dict(category_list):
#         category_dit = {}
#         for k, v in CategoryStatus.__members__.items():
#             if v.value in category_list:
#                 k = k.replace("_", " ").title()
#                 category_dit[v.value] = k
#         return category_dit


class Category(models.Model, Model):
    CATEGORY_STATUS = EnumBase.get_model_status(CategoryEn, CategoryZh)
    com_id = models.IntegerField(null=False, verbose_name="漫画ID")
    category = models.IntegerField(default=0, choices=CATEGORY_STATUS, verbose_name="漫画分类")

    class Meta:
        verbose_name_plural = "分类信息"
        app_label = "api"

    def show_default_comics_name(self):
        from api.models import Search
        title = Search.get(com_id=self.com_id).en_title
        return title if title else "空"

    show_default_comics_name.__name__ = "漫画名"

    # def change_category(self):
    #     from api.models import CategoryStatus
    #     c_k = [i for i in CategoryStatus.__members__.keys()]
    #     c_v = [i.value for i in CategoryStatus.__members__.values()]
    #     c = dict(zip(c_v, c_k))
    #     if self.category in c_v:
    #         return c[self.category]
    #
    # change_category.__name__ = "漫画分类"
