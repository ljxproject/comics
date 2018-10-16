
import django

from adminx.helpers.piece import get_order_parm

django.setup()

from comic.celery import app
from adminx.models import OrderStatisticDetail, OrderStatistic


@app.task
def order_statistics():
    today, income, expect_income, paid_order, no_paid_order, expired_order, total_order = get_order_parm()
    # 存入订单统计详情表中
    OrderStatisticDetail(income=income, expect_income=expect_income, paid_order=paid_order,
                         no_paid_order=no_paid_order, expired_order=expired_order, total_order=total_order).save()
    # 修改订单统计表简要表
    # if today.day == 1:
    m = today.month
    d = today.day
    l = [1, 4, 7, 10]
    # 如果日期为日期为1.1,4.1,7.1,10.1则name=3数据置0
    if m in l and d == 1:
        delete_os(3)
    # 如果日期为每月一号则name=2数据置0
    elif d == 1:
        delete_os(2)
    name_list = [1, 2, 3, 4]
    exist_list = OrderStatistic.objects.filter(name__in=name_list)
    exist_name_list = []
    for o in exist_list:
        exist_name_list.append(o.name)
        if o.name == 1:
            o.income = income
            o.paid_order = paid_order
            o.no_paid_order = no_paid_order
            o.expired_order = expired_order
            o.total_order = total_order
            o.save()
        else:
            o.income = str(float(o.income) + float(income))
            o.paid_order += paid_order
            o.no_paid_order += no_paid_order
            o.expired_order += expired_order
            o.total_order += total_order
            o.save()
    not_exist_list = list(set(name_list).difference(set(exist_name_list)))
    for name in not_exist_list:
        OrderStatistic(name=name, income=income, paid_order=paid_order,
                       no_paid_order=no_paid_order, expired_order=expired_order,
                       total_order=total_order).save()
    print("Finish")


def delete_os(name):
    OrderStatistic(name=name, no_paid_order=0, expired_order=0,
                   total_order=0, income="0", paid_order=0).save()
