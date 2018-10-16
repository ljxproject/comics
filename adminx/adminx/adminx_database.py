import datetime

import markdown as markdown
from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import formats, timezone

from adminx.forms import CDBForm
from adminx.helpers.backup_handler import backup
from adminx.helpers.piece import get_key_dict, sum_size
from xadmin import views, site, sites
from adminx.helpers import MyPaginator, datbase
from xadmin.util import template_localtime
from adminx.models import DataBackup


class TablesAdminView(views.CommAdminView):
    list_per_page = None
    remove_permissions = []

    def __init__(self, request, *args, **kwargs):
        self.model = DataBackup
        self.opts = self.model._meta
        self.app_label = self.model._meta.app_label

        super(TablesAdminView, self).__init__(request, *args, **kwargs)

    def has_change_permission(self, obj=None):
        codename = get_permission_codename('change', self.opts)
        return ('change' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))

    def get(self, request, *args, **kwargs):
        if self.has_change_permission():
            permission = True
        else:
            permission = False
        cur_page = int(request.GET.get("page", 1))
        datbase_data = datbase.bkdb_all()
        for i in datbase_data:
            if isinstance(i["create_time"], datetime.datetime):
                i["create_time"] = formats.localize(template_localtime(timezone.make_aware(i["create_time"])))
            if isinstance(i["update_time"], datetime.datetime):
                i["update_time"] = formats.localize(template_localtime(timezone.make_aware(i["update_time"])))
            i["editor"] = i["table_name"] + "/?next=" + request.get_full_path()
            string_list = [i["data_size"], i["index_size"]]
            i["size_MB"] = sum_size(string_list)

        p = MyPaginator(datbase_data, self.list_per_page)
        data = p.get_p_obj(cur_page)
        count = len(datbase_data)
        page_range = p.get_page_range(cur_page)
        context = super(TablesAdminView, self).get_context()
        menu = context["admin_view"].get_site_menu()
        title = "数据库表"
        re = get_key_dict(menu, "title", title)
        icon = re["icon"]
        context["breadcrumbs"].append({"url": "/xadmin/test", "title": title})
        context.update({"data": data, "page_range": page_range, "count": count,
                        "title": title, "icon": icon, "permission": permission})

        return render(request, 'database/tables.html', context)


site.register_view(r'^database/$', TablesAdminView, name='database')


class CDBEditorAdminView(views.CommAdminView):

    def get(self, request, *args, **kwargs):
        form = CDBForm()
        redirect_to = request.GET.get('next', '')
        table = kwargs.get("path", "")
        data = datbase.show_cdb_create(table)[0]["Create Table"].replace(",", ",\n")
        data = markdown.markdown(data,
                                 extensions=[
                                     'markdown.extensions.fenced_code'
                                 ])
        context = super(CDBEditorAdminView, self).get_context()
        context.update({"data": data, "next": redirect_to, "form": form})
        return render(request, 'database/cdb_editor.html', context)

    def post(self, request, *args, **kwargs):
        form = CDBForm(request.POST)
        form.is_valid()
        redirect_to = request.GET.get('next', '')
        table = kwargs.get("path", "")
        data = datbase.show_cbd_create(table)[0]["Create Table"].replace(",", ",\n")
        data = markdown.markdown(data,
                                 extensions=[
                                     'markdown.extensions.fenced_code'
                                 ])
        context = super(CDBEditorAdminView, self).get_context()
        context.update({"data": data, "next": redirect_to, "form": form})
        return render(request, 'database/cdb_editor.html', context)


site.register_view(r'^database/(?P<path>\w*)/$', CDBEditorAdminView, name='detail')


@sites.register(TablesAdminView)
class TablesAdmin(object):
    list_per_page = 20


class DataBackupAdminView(views.CommAdminView):

    def get(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next', '')
        basedir = request.GET.get("basedir", "")
        base = request.GET.get("base", "")
        backup_type = int(request.GET.get("backup_type", ""))
        if basedir:
            re = backup.backup(backup_type, basedir)
        else:
            re = backup.backup(backup_type)
        context = super(DataBackupAdminView, self).get_context()
        if isinstance(re, Exception):
            messages.error(request, re)
            context.update({"messages": messages})
        else:
            bk = DataBackup(name=re[1], backup_type=backup_type,
                            backup_file=re[2], size=re[0])
            if base:
                bk.base = base
            bk.save()
            messages.success(request, "已完成备份: %s, 请完善该备份备注" % re[1])
            context.update({"messages": messages})
        return redirect(redirect_to)


site.register_view(r'^adminx/databackup/backup/$', DataBackupAdminView, name='db_backup')


@sites.register(DataBackup)
class DataBackupAdmin(object):
    db_backup = True
    list_display = ["id", "name", "size", "backup_type", "backup_file", "comment", "created", "modified", "base"]
    list_filter = ["id", "name", "backup_type", "created", "modified", "base"]
    list_per_page = 20
