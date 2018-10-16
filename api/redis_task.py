import django
import time
import datetime
import pytz

django.setup()

from django.db.models import Q
from django.utils import timezone

from api.models import ComicInfo, Category, ImgResource
from comic.celery import app
from api.helpers import r
from userapi.models import Permission


@app.task
def redis_to_mysql():
    # 读取redis权限表
    email_list_iter = r.scan_iter("*_authority", 1)
    for email_b in email_list_iter:
        comics_list_iter = r.hscan_iter(email_b, "*", 1)
        email = bytes.decode(email_b).split("_")[0]
        for comics_b in comics_list_iter:
            comics = eval(comics_b[0])
            chapter_list = eval(comics_b[1])
            free_chap = ComicInfo.get(com_id=comics).free_chapter
            free_list = [i + 1 for i in range(free_chap)]
            purchase_list = list(set(chapter_list).difference(set(free_list)))
            update_list = []
            # 获取需要插入的chapter列表
            for i in purchase_list:
                # 对比mysql数据
                re = Permission.objects.filter(email=email, com_id=comics, chap_id=i).exists()
                if not re:
                    update_list.append(i)
            # 将变化的数据存入mysql
            queryset_list = []
            for i in update_list:
                queryset_list.append(Permission(email=email, com_id=comics, chap_id=i))
            Permission.objects.bulk_create(queryset_list)
    return print("Finish")


@app.task
def create_trend_comics():
    # 存在的热门推荐列表置换category表
    exist_trend_list = ComicInfo.filter(category=3)
    for i in exist_trend_list:
        com_id = i.com_id
        i.category = Category.get(com_id=com_id).category
        i.modified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        i.save()
    # ComicInfo 根据download排序取前4
    trend_list = ComicInfo.objects.filter(Q(status__gt=1001) & Q(download__gt=0)).order_by("-download")[:4]
    # 更改其分类
    for comics in trend_list:
        if comics.category != 1:  # 非主编推荐
            comics.category = 3
            comics.modified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
            comics.save()
    return print("create trend finish")


@app.task
def change_free_permission_and_imgresource():
    # 提取修改时间在一周内的漫画
    utc_now = datetime.datetime.now(tz=timezone.utc)
    utc_week = utc_now - datetime.timedelta(2)
    comics_list = ComicInfo.filter(modified__gte=utc_week)
    # 读取其free_chapter
    for comics in comics_list:
        com_id = comics.com_id
        free_chapter = comics.free_chapter
        for j in range(free_chapter):
            # 更改imgresource
            ImgResource.filter(com_id=com_id, chap_id=j + 1).update(price="0.00")
    return print("free chapter finish")
