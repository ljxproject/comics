from django.test import TestCase

from enum import unique, Enum


class EnumBase(object):
    error_dict = {}
    category_dict = {}
    comic_dict = {}

    @staticmethod
    def _get_name():
        pass

    @classmethod
    def set_d(cls):
        for i in EnumBase.__subclasses__():
            tp, lang = cls.get_dict(i)
            if tp == "error":
                EnumBase.error_dict[lang] = i
            elif tp == "category":
                EnumBase.category_dict[lang] = i
            elif tp == "comic":
                EnumBase.comic_dict[lang] = i

    @classmethod
    def get_status_obj(cls, o, name):
        obj = getattr(o, name)
        return obj

    @classmethod
    def get_dict(cls, o):
        name = o._get_name()
        return tuple(name.split("_"))

    @classmethod
    def get_status(cls, i, o, lang="en"):
        name = o.get_name_from_value(i)
        tp = cls.get_dict(o)[0]
        dic = getattr(EnumBase, "%s_dict" % tp)
        obj = dic[lang]
        obj = cls.get_status_obj(obj, name)
        value = i
        name = obj.value.replace("_", " ").title()
        status = {
            "status": value,
            "msg": name
        }
        return status

    @classmethod
    def get_status_default_name(cls, i, o):
        name = o.get_name_from_value(i).replace("_", " ").title()
        return name



@unique
class CategoryZh(EnumBase, Enum):
    """主编推荐"""
    editor_recommend = 1
    """完结推荐"""
    finish_recommend = 2
    """热门推荐"""
    trend_recommend = 3
    """中漫"""
    manhua = 10
    """日漫"""
    manga = 11

    @staticmethod
    def _get_name():
        return "category_zh"

    @staticmethod
    def get_name_from_value(num):
        for i in CategoryZh.__members__.values():
            if i.value == num:
                return i.name


@unique
class CategoryMy(EnumBase, Enum):
    """主编推荐"""
    editor_recommend = "my_ed"
    """完结推荐"""
    finish_recommend = "my_fi"
    """热门推荐"""
    trend_recommend = "my_tr"
    """中漫"""
    manhua = "my_mh"
    """日漫"""
    manga = "my_mg"

    @staticmethod
    def _get_name():
        return "category_my"


@unique
class CategoryEy(EnumBase, Enum):
    """主编推荐"""
    editor_recommend = "ey_ed"
    """完结推荐"""
    finish_recommend = "ey_fi"
    """热门推荐"""
    trend_recommend = "ey_tr"
    """中漫"""
    manhua = "ey_mh"
    """日漫"""
    manga = "ey_mg"

    @staticmethod
    def _get_name():
        return "category_en"


@unique
class ComicZh(EnumBase, Enum):
    """空"""
    none = 0
    """已完结"""
    finish = 1001
    """连载中"""
    serial = 1002
    """免费"""
    free = 1003

    @staticmethod
    def _get_name():
        return "comic_zh"

    @staticmethod
    def get_name_from_value(num):
        for i in ComicZh.__members__.values():
            if i.value == num:
                return i.name


@unique
class ComicMy(EnumBase, Enum):
    """空"""
    none = "my_n"
    """已完结"""
    finish = "my_f"
    """连载中"""
    serial = "my_se"
    """免费"""
    free = "my_fr"

    @staticmethod
    def _get_name():
        return "comic_my"


# @unique
# class EN(EnumBase, Enum):
#     name = "AAA"
#     age = 10
#
#     # pass
#     @staticmethod
#     def __get_name__():
#         return "error_en"
#
#
# @unique
# class ZH(EnumBase, Enum):
#     name = 100
#
#     @staticmethod
#     def get_name_from_value(num):
#         for i in ZH.__members__.values():
#             if i.value == num:
#                 return i.name


EnumBase.set_d()

# print(EnumBase.get_category_status(2))
# print(EnumBase.get_category_status(2,"my"))
# print(EnumBase.get_comic_status(1002, "my"))
