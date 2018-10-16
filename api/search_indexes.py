from haystack import indexes

from api.models import Search


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # 获取模型
    def get_model(self):
        return Search

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

