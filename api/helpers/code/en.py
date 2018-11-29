from enum import Enum, unique

from api.helpers.myenum import EnumBase


@unique
class CategoryEn(EnumBase, Enum):
    """其他分类"""
    other = 0
    """主编推荐"""
    editor_recommend = 1
    """完结推荐"""
    finished_recommend = 2
    """热门推荐"""
    trend_recommend = 3
    """中漫"""
    manhua = 10
    """日漫"""
    manga = 11

    @staticmethod
    def _get_name():
        return "category_en"

    @staticmethod
    def get_name_from_value(num):
        for i in CategoryEn.__members__.values():
            if i.value == num:
                return i.name


@unique
class ComicEn(EnumBase, Enum):
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
        return "comic_en"

    @staticmethod
    def get_name_from_value(num):
        for i in ComicEn.__members__.values():
            if i.value == num:
                return i.name


@unique
class CodeEn(EnumBase, Enum):
    """成功"""
    success = 600
    """添加收藏成功"""
    collect_success = 601
    """取消收藏成功"""
    delete_collection_success = 602
    """暂无此漫画"""
    comics_not_found = 620
    """该漫画暂无此章节"""
    chapter_not_found = 621
    """暂无此类漫画"""
    this_category_of_comic_do_not_exist = 622
    """该章节免费"""
    this_chapter_has_been_freed = 623
    """该章节已购"""
    this_chapter_has_been_purchased = 624
    """无该语言漫画"""
    this_comics_has_not_localization = 628
    """无该语言章节"""
    this_chapter_has_not_localization = 629
    """该用户暂无此章节权限"""
    this_chapter_has_not_been_purchased = 630
    """该用户未购任何漫画"""
    it_seems_you_have_not_any_purchased_comics_yet = 631
    """该用户已存在"""
    user_existed = 632
    """该用户不存在"""
    user_not_found = 633
    """该用户并未登录"""
    you_are_offline_in_this_device = 634
    """该用户余额不足"""
    insufficient_fund = 635
    """该用户信息更改失败"""
    modify_failed = 636
    """该用户注册登录失败"""
    sign_in_failed = 637
    """该用户验证失败"""
    captcha_not_match = 638
    """该用户邮箱信息有误"""
    email_error = 639
    """此邮箱已绑定"""
    this_email_has_been_bound = 640
    """图片不合法"""
    invalied_image = 641
    """暂无此语言"""
    invalied_language = 642
    """暂无评论"""
    this_comics_has_not_comment = 643
    """发布评论失败"""
    release_comment_failed = 644
    """未知错误"""
    unknown_error = 660

    @staticmethod
    def _get_name():
        return "code_en"

    @staticmethod
    def get_name_from_value(num):
        for i in CodeEn.__members__.values():
            if i.value == num:
                return i.name



