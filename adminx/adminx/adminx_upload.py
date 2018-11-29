import os
import time

from django.contrib import messages
from django.shortcuts import render, redirect,HttpResponse
from django.conf import settings
from django.http import JsonResponse

import xadmin
from adminx.forms import MangaUploadForm
from adminx.helpers import mangaupload, get_key_dict, p_b
from adminx.helpers.piece import s_to_time, remove_temp_file
from adminx.models import MangaUpload, DataBackup
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
        upload_file = request.FILES.get('file', "")
        task = request.POST.get('task_id')  # 获取文件唯一标识符
        chunk = request.POST.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = os.path.join(settings.RESOURCES_PATH, 'temp', '%s_%s') % (task, chunk)
        with open(filename, 'wb') as wf:
            wf.write(upload_file.read())
        # form = MangaUploadForm()
        # context = super(MangaUploadAdminView, self).get_context()
        # context.update({"messages": messages})
        # menu = context["admin_view"].get_site_menu()
        # title = "漫画上传"
        # re = get_key_dict(menu, "title", title)
        # icon = re["icon"]
        # url = re["url"]
        # context["breadcrumbs"].append({"url": url, "title": title})
        # context.update({"form": form, "title": title, "icon": icon})
        # return render(request, 'mangaupload/mangaupload.html', context)
        return HttpResponse("OK")

site.register_view(r'^mangaupload/$', MangaUploadAdminView, name='mangaupload')


class MangaUploadSuccess(CommAdminView):
    def get(self, request, *args, **kwargs):
        st = float(request.GET.get("st", "")) * 0.001
        form = MangaUploadForm()
        context = super(MangaUploadSuccess, self).get_context()
        menu = context["admin_view"].get_site_menu()
        title = "漫画上传"
        re = get_key_dict(menu, "title", title)
        icon = re["icon"]
        url = re["url"]
        context["breadcrumbs"].append({"url": url, "title": title})
        key = request.GET.get("key", "")
        redirect_to = request.GET.get("next", '')
        target_filename = request.GET.get('filename')  # 获取上传文件的文件名
        task = request.GET.get('task_id')  # 获取文件的唯一标识符

        chunk = 0  # 分片序号
        tg_path = os.path.join(settings.RESOURCES_PATH, target_filename)
        if os.path.exists(tg_path):
            # return JsonResponse(data={"H":"OK"})
            cost_time = time.time() - st
            humen_time = s_to_time(cost_time)
            p_b.write(key, 100, "总耗时：%s" % humen_time)
            remove_temp_file(os.path.join(settings.RESOURCES_PATH, 'temp'), task)
            messages.error(request, "错误：存在同名文件")
            context.update({"form": form, "title": title, "icon": icon, "next": redirect_to})
            return render(request, 'mangaupload/mangaupload.html', context)
        else:
            p_b.write(key, 50, "开始处理文件")
            with open(tg_path, 'wb') as target_file:  # 创建新文件
                while True:
                    try:
                        filename = os.path.join(settings.RESOURCES_PATH, 'temp', '%s_%d') % (task, chunk)
                        source_file = open(filename, 'rb')  # 按序打开每个分片
                        target_file.write(source_file.read())  # 读取分片内容写入新文件
                        source_file.close()
                    except IOError:
                        break
                    chunk += 1
                    os.remove(filename)
            p_b.write(key, 60, "开始执行漫画SDK包")
            err = mangaupload.manga_upload(tg_path)
            if not err:
                p_b.write(key, 90, "正在检查错误日志")
                err = mangaupload.show_manga_errors()
                cost_time = time.time() - st
                humen_time = s_to_time(cost_time)
                p_b.write(key, 100, "总耗时：%s" % humen_time)
                if not err:
                    mu = MangaUpload(name=target_filename, resources_file=tg_path)
                    mu.save()
                    return JsonResponse(data={"url": redirect_to})
            err = "错误：" + err
            os.remove(tg_path)
        cost_time = time.time() - st
        humen_time = s_to_time(cost_time)
        p_b.write(key, 100, "总耗时：%s" % humen_time)
        context.update({"form": form, "title": title, "icon": icon, "next": redirect_to, 'err': err})
        return render(request, 'mangaupload/mangaupload.html', context)


site.register_view(r'^mangaupload-success/$', MangaUploadSuccess, name='mangaupload_success')


@xadmin.sites.register(MangaUpload)
class MangaUploadAdmin(object):
    manga_upload = True
    list_display = ["name", "resources_file", "created"]
    list_per_page = 5
    model_icon = 'fa fa-upload'
