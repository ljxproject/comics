from enum import Enum, unique

from api.helpers.myenum import EnumBase


@unique
class CategoryMs(EnumBase, Enum):
    """其他分类"""
    other = "Lain-lain"
    """主编推荐"""
    editor_recommend = "Syor Penyunting"
    """完结推荐"""
    finished_recommend = "Syor Tamat"
    """热门推荐"""
    trend_recommend = "Syor Panas"
    """中漫"""
    manhua = "Manga Cina"
    """日漫"""
    manga = "Manga Jepun"

    @staticmethod
    def _get_name():
        return "category_ms"


@unique
class ComicMs(EnumBase, Enum):
    """空"""
    none = "Kosong"
    """已完结"""
    finish = "Telah Tamat"
    """连载中"""
    serial = "Akan bersambung"
    """免费"""
    free = "Percuma"

    @staticmethod
    def _get_name():
        return "comic_ms"


@unique
class CodeMs(EnumBase, Enum):
    """成功"""
    success = "Berjaya"
    """添加收藏成功"""
    collect_success = "berjaya ditambah ke koleksi"
    """取消收藏成功"""
    delete_collection_success = "pembatalan koleksi berjaya"
    """暂无此漫画"""
    comics_not_found = "Tiada manga ini sementara"
    """该漫画暂无此章节"""
    chapter_not_found = "Manga ini tiada bab ini sementara"
    """暂无此类漫画"""
    this_category_of_comic_do_not_exist = "Tiada manga kategori ini sementara"
    """该章节免费"""
    this_chapter_has_been_freed = "Bab ini percuma"
    """该章节已购"""
    this_chapter_has_been_purchased = "Bab ini sudah di beli"
    """无该语言漫画"""
    this_comics_has_not_localization = "Tiada manga bahasa ini"
    """无该语言章节"""
    this_chapter_has_not_localization = "Tiada bab bahasa ini"
    """该用户暂无此章节权限"""
    this_chapter_has_not_been_purchased = "Pengguna tiada akses ke bab ini"
    """该用户未购任何漫画"""
    it_seems_you_have_not_any_purchased_comics_yet = "Pengguna belum membeli sebarang manga"
    """该用户已存在"""
    user_existed = "Pengguna sudah wujud"
    """该用户不存在"""
    user_not_found = "Pengguna belum wujud"
    """该用户并未登录"""
    you_are_offline_in_this_device = "Pengguna belum log masuk"
    """该用户余额不足"""
    insufficient_fund = "Baki pengguna tidak mencukupi"
    """该用户信息更改失败"""
    modify_failed = "Maklumat pengguna gagal diubah"
    """该用户注册登录失败"""
    sign_in_failed = "Pengguna gagal log masuk/daftar"
    """该用户验证失败"""
    captcha_not_match = "Pengesahan pengguna gagal"
    """该用户邮箱信息有误"""
    email_error = "Emel pengguna tidak tepat"
    """此邮箱已绑定"""
    this_email_has_been_bound = "Emel ini telah diikat"
    """图片不合法"""
    invalied_image = "Gambar tidak sah"
    """暂无此语言"""
    invalied_language = "Tiada bahasa ini sementara"
    """发布评论失败"""
    release_comment_failed = "ulasan gagal disiarkan"
    """未知错误"""
    unknown_error = "Ralat tidak diketahui"

    @staticmethod
    def _get_name():
        return "code_ms"

    @staticmethod
    def get_name_from_value(num):
        for i in CodeMs.__members__.values():
            if i.value == num:
                return i.name
