import os
import datetime

from django.db.models import Sum
from django.utils import timezone

from userapi.models import Transaction


def get_key_dict(l, key, value):
    for i in l:
        if key in i:
            if i[key] == value:
                return i
        values = i.values()
        for v in values:
            if isinstance(v, list):
                re = get_key_dict(v, key, value)
                if re:
                    return re
            else:
                continue


def sum_size(string_list):
    sum = 0
    for i in string_list:
        i = i.replace("MB", "").strip()
        sum += float(i)
    size = str(sum) + "MB"
    return size


def get_order_parm(is_today=None):
    if is_today:
        day = datetime.datetime.today()
    else:
        day = datetime.datetime.today() - datetime.timedelta(days=1)
    created_date = timezone.make_aware(datetime.datetime(day.year, day.month, day.day, 0, 0, 0))
    base_query_set = Transaction.filter(created__gte=created_date)

    total_order = base_query_set.count()
    expect_income = str(base_query_set.aggregate(expect_income=Sum('gmv'))['expect_income'])
    no_paid_order = base_query_set.filter(status=0).count()
    paid_order = base_query_set.filter(status=1).count()
    pre_income = base_query_set.filter(status=1).aggregate(income=Sum('gmv'))['income']
    income = str(pre_income if pre_income else "0")
    expired_order = total_order - paid_order - no_paid_order
    return day, income, expect_income, paid_order, no_paid_order, expired_order, total_order


def s_to_time(seconds):
    m, s = divmod(seconds, 60)
    if m >= 60:
        h, m = divmod(m, 60)
        return ("%02d:%02d:%02d" % (h, m, s))
    return ("%02d:%02d" % (m, s))


def remove_temp_file(path, string):
    for file in os.listdir(path):
        if file.startswith(string):
            os.remove(os.path.join(path, file))
