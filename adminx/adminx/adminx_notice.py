
import xadmin
from adminx.models import Notice


@xadmin.sites.register(Notice)
class NoticeAdmin(object):
    list_display = ["name", "file", "created"]
    list_per_page = 10
    hidden_menu = True

