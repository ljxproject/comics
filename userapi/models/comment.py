from django.db import models

from api.models.self_model import Model


class Comment(models.Model, Model):
    com_id = models.IntegerField(verbose_name="漫画ID")
    title = models.CharField(max_length=32, verbose_name="评论标题")
    content = models.CharField(max_length=256, verbose_name="评论内容")
    rate = models.CharField(default="0", max_length=5, verbose_name="评论评分")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_delete = models.BooleanField(default=0, verbose_name="是否撤回")
    email = models.CharField(max_length=64, verbose_name="用户邮箱")
    lang = models.CharField(max_length=10, verbose_name="评论语言")

    class Meta:
        verbose_name_plural = "漫画评论信息"
        app_label = "userapi"

    def show_default_comics_name(self):
        from api.models import Search
        title = Search.get(com_id=self.com_id).ms_title
        return title if title else "空"

    show_default_comics_name.__name__ = "漫画名"
