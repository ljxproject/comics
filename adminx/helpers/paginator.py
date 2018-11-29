import math

from django.core.paginator import Paginator


class MyPaginator(object):
    paginator_class = Paginator

    def __init__(self, items, list_per_page):
        self.paginator = self.get_p(items, list_per_page)

    def get_p(self, items, list_per_page):
        return self.paginator_class(items, list_per_page)

    def get_p_obj(self, cur_page):
        if cur_page:
            obj = self.paginator.page(cur_page)
        else:
            obj = self.paginator.page(1)
        return obj

    def get_total_page(self):
        return self.paginator.num_pages

    # 定义一个分页的函数
    def get_page_range(self, cur_page):
        # current_page: 表示当前页
        # total_page: 表示总页数。
        # max_page： 表示最大显示页数。
        total_page = self.paginator.num_pages
        max_page = 10
        middle = math.ceil(max_page / 2)
        # 如果总页数 小于 最大显示页数。
        # 特殊情况
        if total_page < max_page:
            start = 1
            end = total_page
        else:
            # 正常情况
            # 第一种：当前页在头部的时候。
            if cur_page <= middle:
                start = 1
                end = max_page
                # 第二种情况： 当前页在中间的位置
            elif (cur_page > middle) and (cur_page < total_page - middle):
                start = cur_page - middle
                end = cur_page + middle - 1
            else:
                # 第三种情况， 当前页在尾巴
                start = total_page - max_page + 1
                end = total_page

        return range(start, end + 1)
