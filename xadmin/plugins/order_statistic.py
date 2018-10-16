from django.template import loader

from adminx.helpers.piece import get_order_parm
from adminx.models import OrderStatistic
from xadmin import site
from xadmin.views import BaseAdminPlugin, ListAdminView


class OrderStatisticPlugin(BaseAdminPlugin):
    order_statistic = False

    def init_request(self, *args, **kwargs):
        return bool(self.order_statistic)

    def get_self_model(self):
        model = OrderStatistic
        today, income, expect_income, paid_order, no_paid_order, expired_order, total_order = get_order_parm()
        name_list = [0, 1, 2, 3, 4]
        for name in name_list:
            if not model.objects.filter(name=name).exists():
                model(name=name, income=income, paid_order=paid_order, no_paid_order=no_paid_order,
                      expired_order=expired_order,
                      total_order=total_order).save()
        model.objects.filter(name=0).update(income=income, paid_order=paid_order, no_paid_order=no_paid_order,
                                            expired_order=expired_order,
                                            total_order=total_order)
        o = model.objects.all()
        for i in o:
            if i.total_order == 0:
                i.complete = 0
            else:
                i.complete = '%.1f' % (int(i.paid_order) / int(i.total_order) * 100)
        return o

    def block_results_top(self, context, nodes):
        model = self.get_self_model()
        nodes.append(loader.render_to_string('statistics/order_statistic.html', {'data': model}))

    def block_extrahead(self, context, nodes):
        js = '<script src="https://img.hcharts.cn/highcharts/highcharts.js"></script>'
        js += '<script src="https://img.hcharts.cn/highcharts/modules/exporting.js"></script>'
        nodes.append(js)


site.register_plugin(OrderStatisticPlugin, ListAdminView)
