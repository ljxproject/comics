from django.contrib import admin

# Register your models here.

import xadmin
from api.models import Search, ComicInfo, ImgResource, ComicStatus, Category


@xadmin.sites.register(ComicInfo)
class ComicsAdmin(object):
    list_display = ['com_id', 'show_default_comics_name', 'free_chapter', 'total_chapter',
                    'download', 'created', 'modified', 'change_status', 'change_category']
    search_field = ['com_id', 'download', 'status', 'category',
                    'created', 'modified']
    list_filter = ['com_id', 'download', 'status', 'category',
                   'created', 'modified']
    list_per_page = 20
    model_icon = 'fa fa-book'


@xadmin.sites.register(ImgResource)
class ImgResourceAdmin(object):
    list_display = ["com_id", "show_default_comics_name", "chap_id", "my_title", "price"]
    list_filter = ["com_id", "chap_id", "price"]
    list_per_page = 20
    model_icon = 'fa fa-info'


@xadmin.sites.register(Search)
class SearchAdmin(object):
    list_display = ["com_id", "my_title", "my_author", "my_subtitle", "my_introduction"]
    list_per_page = 20
    model_icon = 'fa fa-search'


@xadmin.sites.register(Category)
class CategoryAdmin(object):
    list_display = ["com_id", "show_default_comics_name", "change_category"]
    list_filter = ["com_id", "category"]
    list_per_page =20
    model_icon = 'fa fa-sitemap'