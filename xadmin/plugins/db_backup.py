import os

from django.contrib import messages

from adminx.helpers import datbase
from xadmin import site
from xadmin.views import BaseAdminPlugin, ListAdminView


class DBBackupPlugin(BaseAdminPlugin):
    db_backup = False

    def init_request(self, *args, **kwargs):
        return bool(self.db_backup)

    def incremental_and_differential_backup(self, instance):
        backup_type = instance.backup_type
        basedir = instance.backup_file
        base = instance.id
        str_url = '%sbackup/?next=%s&basedir=%s&base=%d' % \
                  (self.request.path, self.request.path, basedir, base)
        if backup_type == 0:
            return u"<a href=%s&backup_type=1>差异备份</a>" % str_url
        else:
            return u"<a href=%s&backup_type=2>增量备份</a>" % str_url

    incremental_and_differential_backup.short_description = '操作'
    incremental_and_differential_backup.allow_tags = True

    def get_list_display(self, list_display):
        # if self.has_delete_permission():
        list_display.append("incremental_and_differential_backup")
        self.admin_view.incremental_and_differential_backup = self.incremental_and_differential_backup
        return list_display

    def block_nav_btns(self, context, nodes):
        size = os.popen("du -sh /usr/local/mysql/data/ |cut -d '/' -f 1").readlines()[0]

        messages.info(self.request, "恢复数据请联系运维人员")
        btn = "<div>数据库总空间大小:%s</div>" % size
        btn += "<a href='%sbackup/?backup_type=0&next=%s' class='btn btn-primary'>完全备份</a>" % (
            self.request.path, self.request.path)
        nodes.append(btn)


site.register_plugin(DBBackupPlugin, ListAdminView)
