import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_permission_codename

from xadmin import site
from xadmin.views import BaseAdminPlugin, ListAdminView


class DBBackupPlugin(BaseAdminPlugin):
    db_backup = False

    def has_change_permission(self, obj=None):
        codename = get_permission_codename('change', self.model._meta)
        return self.request.user.has_perm('%s.%s' % (self.model._meta.app_label, codename))

    def init_request(self, *args, **kwargs):
        if self.has_change_permission():
            return bool(self.db_backup)
        return False

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
        list_display.append("incremental_and_differential_backup")
        self.admin_view.incremental_and_differential_backup = self.incremental_and_differential_backup
        return list_display

    def block_nav_btns(self, context, nodes):
        # size = os.popen("sudo du -sh %s |cut -d '/' -f 1" % settings.MYSQL_DATA_PATH).readlines()[0]
        size = os.popen("du -sh %s |cut -d '/' -f 1" % settings.MYSQL_DATA_PATH).readlines()[0]  # mac
        messages.info(self.request, "恢复数据请联系运维人员")
        btn = "<div>数据库总空间大小:%s</div>" % size
        btn += "<a href='%sbackup/?backup_type=0&next=%s' class='btn btn-primary'>完全备份</a>" % (
            self.request.path, self.request.path)

        nodes.append(btn)


site.register_plugin(DBBackupPlugin, ListAdminView)
