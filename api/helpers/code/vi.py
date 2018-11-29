from enum import Enum, unique

from api.helpers.myenum import EnumBase


@unique
class CategoryVi(EnumBase, Enum):
    """其他分类"""
    other = "Thể loại khác"
    """主编推荐"""
    editor_recommend = "Biên tập viên tiến cử"
    """完结推荐"""
    finished_recommend = "Đã hoàn chỉnh"
    """热门推荐"""
    trend_recommend = "Đang hot"
    """中漫"""
    manhua = "Truyện Trung Quốc"
    """日漫"""
    manga = "Truyện Nhật Bản"

    @staticmethod
    def _get_name():
        return "category_vi"


@unique
class ComicVi(EnumBase, Enum):
    """空"""
    none = "Trống"
    """已完结"""
    finish = "Đã hoàn chỉnh"
    """连载中"""
    serial = "Đang đăng"
    """免费"""
    free = "Miễn phí"

    @staticmethod
    def _get_name():
        return "comic_vi"


@unique
class CodeVi(EnumBase, Enum):
    """成功"""
    success = "Thành công"
    """添加收藏成功"""
    collect_success = "Thêm yêu thích thành công"
    """取消收藏成功"""
    delete_collection_success = "Xóa yêu thích thành công"
    """暂无此漫画"""
    comics_not_found = "Tạm không có truyện này"
    """该漫画暂无此章节"""
    chapter_not_found = "Truyện tạm không có chương này"
    """暂无此类漫画"""
    this_category_of_comic_do_not_exist = "Tạm không có truyện thể loại này"
    """该章节免费"""
    this_chapter_has_been_freed = "Chương này miễn phí"
    """该章节已购"""
    this_chapter_has_been_purchased = "Chương này đã mua"
    """无该语言漫画"""
    this_comics_has_not_localization = "Không có truyện ngôn ngữ này"
    """无该语言章节"""
    this_chapter_has_not_localization = "Không có chương ngôn ngữ này"
    """该用户暂无此章节权限"""
    this_chapter_has_not_been_purchased = "Tài khoản tạm không có quyền đọc chương này"
    """该用户未购任何漫画"""
    it_seems_you_have_not_any_purchased_comics_yet = "Tài khoản chưa mua truyện nào"
    """该用户已存在"""
    user_existed = "Tài khoản đã tồn tại"
    """该用户不存在"""
    user_not_found = "Tài khoản không tồn tại"
    """该用户并未登录"""
    you_are_offline_in_this_device = "Tài khoản chưa đăng nhập"
    """该用户余额不足"""
    insufficient_fund = "Số dư tài khoản không đủ"
    """该用户信息更改失败"""
    modify_failed = "Thay đổi thông tin tài khoản thất bại"
    """该用户注册登录失败"""
    sign_in_failed = "Tài khoản đăng kí đăng nhập thất bại"
    """该用户验证失败"""
    captcha_not_match = "Xác nhận tài khoản thất bại"
    """该用户邮箱信息有误"""
    email_error = "Lỗi thông tin hộp thư tài khoản"
    """此邮箱已绑定"""
    this_email_has_been_bound = "Email đã ghép"
    """图片不合法"""
    invalied_image = "Hình ảnh không hợp lệ"
    """暂无此语言"""
    invalied_language = "Tạm không có ngôn ngữ này"
    """发布评论失败"""
    release_comment_failed = "Gửi nhận xét thất bại"
    """未知错误"""
    unknown_error = "Lỗi không rõ"

    @staticmethod
    def _get_name():
        return "code_vi"

    @staticmethod
    def get_name_from_value(num):
        for i in CodeVi.__members__.values():
            if i.value == num:
                return i.name
