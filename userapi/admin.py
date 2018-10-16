import xadmin
from django.contrib import admin

from userapi.models import User, PurchaseAndFavorite, Transaction, Permission, FeedBack
from userapi.models.feedback import FeedBackDetail


@xadmin.sites.register(User)
class UserAdmin(object):
    list_display = ["email", "wallet_android", "wallet_ios", "created", "last_online", "login_lock", "bind", "active"]
    list_filter = ["gender", "created", "wallet_ios", "last_online", "wallet_android", "email", "bind", "active"]
    search_field = ["gender", "created", "wallet_ios", "last_online", "wallet_android", "email", "bind"]
    list_per_page = 20
    model_icon = 'fa fa-id-card'


@xadmin.sites.register(PurchaseAndFavorite)
class PFAdmin(object):
    list_display = ["email", "com_id", "show_comics_name", "status"]
    list_filter = ["status", "com_id"]
    list_per_page = 20
    model_icon = 'fa fa-shopping-cart'


@xadmin.sites.register(Transaction)
class TXAdmin(object):
    list_display = ["tx_id", "email", "platform", "gmv",
                    "created", "pay_time", "status"]
    list_filter = ["platform", "gmv", "created", "pay_time", "status"]
    search_field = ["platform", "gmv", "created", "pay_time", "status"]
    list_per_page = 20
    model_icon = 'fa fa-exchange'


@xadmin.sites.register(Permission)
class UserPermissionAdmin(object):
    list_display = ["email", "com_id", "show_comics_name", "chap_id",
                    "show_chapter_name", "show_chap_price", "created"]
    list_filter = ["email", "com_id", "chap_id", "created"]
    search_field = ["email", "com_id", "chap_id", "created"]
    list_per_page = 20
    model_icon = 'fa fa-money'


@xadmin.sites.register(FeedBack)
class FeedBackAdmin(object):
    fb_see = True
    list_display = ["fbd_id", "email", "award", "created", "modified", "status"]
    list_filter = ["email", "award", "created", "modified", "status"]
    list_per_page = 20
    model_icon = 'fa fa-pencil'

