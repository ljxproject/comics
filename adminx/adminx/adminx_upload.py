import os
import time

from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

import xadmin
from adminx.forms import MangaUploadForm
from adminx.helpers import mangaupload, get_key_dict, p_b
from adminx.helpers.piece import s_to_time
from adminx.models import MangaUpload
from xadmin import site
from xadmin.views import CommAdminView


class MangaUploadAdminView(CommAdminView):

    def get(self, request, *args, **kwargs):
        form = MangaUploadForm()
        context = super(MangaUploadAdminView, self).get_context()
        menu = context["admin_view"].get_site_menu()
        title = "漫画上传"
        re = get_key_dict(menu, "title", title)
        icon = re["icon"]
        url = re["url"]
        context["breadcrumbs"].append({"url": url, "title": title})
        context.update({"form": form, "title": title, "icon": icon})
        return render(request, 'mangaupload/mangaupload.html', context)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file", "")
        redirect_to = request.GET.get("next", '')
        key = request.GET.get("key")
        p_b.write(key, 0, "检查文件")
        start_time = time.time()
        if file:
            tg_path = os.path.join(settings.RESOURCES_PATH, file.name)
            if os.path.exists(tg_path):
                messages.error(request, "错误：存在同名文件")
            else:
                p_b.write(key, 10, "开始上传文件")
                with open('%s/%s' % (settings.RESOURCES_PATH, file.name), 'wb') as wf:
                    for chunk in file.chunks():
                        wf.write(chunk)
                p_b.write(key, 50, "开始执行漫画SDK包")
                err = mangaupload.manga_upload(file.name)
                if not err:
                    p_b.write(key, 90, "正在检查错误日志")
                    err = mangaupload.show_manga_errors()
                    cost_time = time.time() - start_time
                    humen_time = s_to_time(cost_time)
                    p_b.write(key, 100, "总耗时：%s" % humen_time)
                    if not err:
                        mu = MangaUpload(name=file.name, resources_file=tg_path)
                        mu.save()
                        return redirect(redirect_to)
                err = "错误：" + err
                os.remove(tg_path)
        cost_time = time.time() - start_time
        humen_time = s_to_time(cost_time)
        p_b.write(key, 100, "总耗时：%s" % humen_time)
        form = MangaUploadForm()
        context = super(MangaUploadAdminView, self).get_context()
        menu = context["admin_view"].get_site_menu()
        title = "漫画上传"
        re = get_key_dict(menu, "title", title)
        icon = re["icon"]
        url = re["url"]
        context["breadcrumbs"].append({"url": url, "title": title})
        context.update({"form": form, "title": title, "icon": icon, "next": redirect_to, 'err': err})
        return render(request, 'mangaupload/mangaupload.html', context)


site.register_view(r'^mangaupload/$', MangaUploadAdminView, name='mangaupload')


@xadmin.sites.register(MangaUpload)
class MangaUploadAdmin(object):
    manga_upload = True
    list_display = ["name", "resources_file", "created"]
    list_per_page = 5
    model_icon = 'fa fa-upload'
