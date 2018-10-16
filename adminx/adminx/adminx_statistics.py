
from adminx.models import OrderStatisticDetail
from xadmin import sites




@sites.register(OrderStatisticDetail)
class OrderStatisticAdmin(object):
    order_statistic = True
    list_display = ['date', 'income', 'expect_income', 'paid_order', 'no_paid_order', 'expired_order', 'total_order']
    list_filter = ['date', 'paid_order', 'no_paid_order', 'expired_order', 'total_order']
    list_per_page = 30
