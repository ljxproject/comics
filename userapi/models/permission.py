from django.db import models

from api.models.self_model import Model


class Permission(models.Model, Model):
    com_id = models.IntegerField(null=False, verbose_name="漫画ID")
    email = models.CharField(max_length=64, null=False, verbose_name="用户邮箱")
    chap_id = models.IntegerField(null=False, verbose_name="章节ID")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "消费信息"
        app_label = "userapi"

    def show_chap_price(self):
        from api.models import ImgResource
        i = ImgResource.get(com_id=self.com_id, chap_id=self.chap_id)
        return i.price
    show_chap_price.__name__ = "消费价格"

    def show_comics_name(self):
        from api.models import Search
        s = Search.get(com_id=self.com_id)
        return s.my_title

    show_comics_name.__name__ = "漫画名"

    def show_chapter_name(self):
        from api.models import ImgResource
        i = ImgResource.get(com_id=self.com_id,chap_id=self.chap_id)
        return i.my_title

    show_chapter_name.__name__ = "漫画章节名"


