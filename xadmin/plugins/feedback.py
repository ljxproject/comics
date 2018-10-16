from xadmin import site
from xadmin.views import BaseAdminPlugin, ListAdminView, filter_hook


class FBSeePlugin(BaseAdminPlugin):
    fb_see = False


    def fb_see_list(self, instance):
        fbd_id = instance.fbd_id
        current_url = self.request.path
        str_url = '/users/feedback/server/%d/?next=%s' % (fbd_id, current_url)

        return u"<a href=%s>查看</a>" % str_url

    fb_see_list.short_description = '操作'
    fb_see_list.allow_tags = True

    def init_request(self, *args, **kwargs):
        return bool(self.fb_see)

    def get_list_display(self, list_display):
        list_display.append("fb_see_list")
        self.admin_view.fb_see_list = self.fb_see_list
        # print(self.model.)
        return list_display
    # def get_context(self, context):
    #     # context.update({"show": "查看"})
    #     # print(context['results'])
    #     return context
    #
    # def block_result_head(self, context, nodes):
    #     return u"<a class='show'>%s</a>" % context['show']


site.register_plugin(FBSeePlugin, ListAdminView)
