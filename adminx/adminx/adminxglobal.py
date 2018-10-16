from django.contrib import admin

# Register your models here.
from django.http import HttpResponse

import xadmin
from adminx.models import DataBackup, MangaUpload, OrderStatisticDetail
from xadmin import views


class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSettings(object):
    # 整体配置
    site_title = 'Manga Burger 后台管理系统'
    site_footer = '顶域科技有限公司'
    menu_style = 'accordion'  # 菜单折叠

    def get_site_menu(self):
        return [
            {
                "title": "数据库管理",
                "icon": 'fa fa-database',
                "menus": [{
                    "title": "数据库表",
                    "icon": "fa fa-list-alt",
                    "url": self.get_admin_url("database"),
                },
                    {
                        "title": "备份",
                        "icon": 'fa fa-repeat',
                        "url": self.get_model_url(DataBackup, "changelist")
                    }
                ]

            },
            {
                "title": "漫画上传系统",
                "icon": 'fa fa-upload',
                "menus": [{
                    "title": "漫画上传",
                    "icon": 'fa fa-upload',
                    "url": self.get_model_url(MangaUpload, "changelist")
                }]
            },
            {
                "title": "数据统计",
                "icon": 'fa fa-bar-chart',
                "menus": [{
                    "title": "订单统计",
                    "icon": 'fa fa-calendar',
                    "url": self.get_model_url(OrderStatisticDetail, "changelist")
                }
                ]
            },
        ]


xadmin.site.register(views.BaseAdminView, BaseSetting)
