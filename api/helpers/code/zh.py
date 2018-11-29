from enum import Enum, unique

from api.helpers.myenum import EnumBase


@unique
class CategoryZh(EnumBase, Enum):
    """其他分类"""
    other = "其他分类"
    """主编推荐"""
    editor_recommend = "主编推荐"
    """完结推荐"""
    finished_recommend = "完结推荐"
    """热门推荐"""
    trend_recommend = "热门推荐"
    """中漫"""
    manhua = "中漫"
    """日漫"""
    manga = "日漫"

    @staticmethod
    def _get_name():
        return "category_Zh"


@unique
class ComicZh(EnumBase, Enum):
    """空"""
    none = "空"
    """已完结"""
    finish = "已完结"
    """连载中"""
    serial = "连载中"
    """免费"""
    free = "免费"

    @staticmethod
    def _get_name():
        return "comic_zh"

@unique
class CodeZh(EnumBase, Enum):
    """成功"""
    success = "成功"
    """添加收藏成功"""
    collect_success = "添加收藏成功"
    """取消收藏成功"""
    delete_collection_success = "取消收藏成功"
    """暂无此漫画"""
    comics_not_found = "暂无此漫画"
    """该漫画暂无此章节"""
    chapter_not_found = "该漫画暂无此章节"
    """暂无此类漫画"""
    this_category_of_comic_do_not_exist = "暂无此类漫画"
    """该章节免费"""
    this_chapter_has_been_freed = "该章节免费"
    """该章节已购"""
    this_chapter_has_been_purchased = "该章节已购"
    """无该语言漫画"""
    this_comics_has_not_localization = "无该语言漫画"
    """无该语言章节"""
    this_chapter_has_not_localization = "无该语言章节"
    """该用户暂无此章节权限"""
    this_chapter_has_not_been_purchased = "该用户暂无此章节权限"
    """该用户未购任何漫画"""
    it_seems_you_have_not_any_purchased_comics_yet = "该用户未购任何漫画"
    """该用户已存在"""
    user_existed = "该用户已存在"
    """该用户不存在"""
    user_not_found = "该用户不存在"
    """该用户并未登录"""
    you_are_offline_in_this_device = "该用户并未登录"
    """该用户余额不足"""
    insufficient_fund = "该用户余额不足"
    """该用户信息更改失败"""
    modify_failed = "该用户信息更改失败"
    """该用户注册登录失败"""
    sign_in_failed = "该用户注册登录失败"
    """该用户验证失败"""
    captcha_not_match = "该用户验证失败"
    """该用户邮箱信息有误"""
    email_error = "该用户邮箱信息有误"
    """此邮箱已绑定"""
    this_email_has_been_bound = "此邮箱已绑定"
    """图片不合法"""
    invalied_image = "图片不合法"
    """暂无此语言"""
    invalied_language = "暂无此语言"
    """暂无评论"""
    this_comics_has_not_comment = "暂无评论"
    """发布评论失败"""
    release_comment_failed = "发布评论失败"
    """未知错误"""
    unknown_error = "未知错误"

    @staticmethod
    def _get_name():
        return "comic_zh"

    @staticmethod
    def get_name_from_value(num):
        for i in CodeZh.__members__.values():
            if i.value == num:
                return i.name