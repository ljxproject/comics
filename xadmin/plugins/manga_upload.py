import uuid

from xadmin import site
from xadmin.views import BaseAdminPlugin, ListAdminView


class MangaUploadPlugin(BaseAdminPlugin):
    manga_upload = False

    def init_request(self, *args, **kwargs):
        return bool(self.manga_upload)

    def block_nav_btns(self, context, nodes):
        next_ = self.get_model_url(self.model, "changelist")
        key = str(uuid.uuid4()).split("-")[1]
        btn = "<a href='/xadmin/mangaupload/?next=%s&key=%s' class='btn btn-primary'>漫画资源上传</a>" % (next_, key)
        nodes.append(btn)


site.register_plugin(MangaUploadPlugin, ListAdminView)
