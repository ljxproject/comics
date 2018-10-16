from enum import Enum, unique


@unique
class Code(Enum):
    """成功"""
    success = 600
    """暂无此漫画"""
    comics_not_found = 620
    """该漫画暂无此章节"""
    chapter_not_found = 621
    """暂无此类漫画"""
    category_do_not_exist = 622
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
    """未知错误"""
    unknown_error = 660

