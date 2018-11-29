from django.conf.urls import url
from api.views import ComicInfoViewSet, get_comics_detail, \
    PurchaseChapterViewSet, get_fuzzy_search_comics, ComicsListViewSet, OwnPurchaseListViewSet, SearchListViewSet, \
    ChapterInfoViewSet, IndexComicsListViewSet, OwnCollectPostViewSet, OwnCollectListViewSet, get_index

urlpatterns = [
    url(r'^comic-information/$', ComicInfoViewSet.as_view({'post': 'post'}), name='get_comics_info'),
    url(r'^chapter-information/$', ChapterInfoViewSet.as_view({'post': 'post'}), name='get_chapters_info'),
    url(r'^comics-list/$', ComicsListViewSet.as_view({'post': 'post'}), name='get_edit_comics'),
    # url(r'^(?i)finish-recommend/$', ComicsListViewSet.as_view({'post': 'list'}), name='get_finish_comics'),
    # url(r'^(?i)trend-recommend/$', ComicsListViewSet.as_view({'post': 'list'}), name='get_trend_comics'),
    # url(r'^(?i)manga/$', ComicsListViewSet.as_view({'post': 'list'}), name='get_manga_comics'),
    # url(r'^(?i)manhua/$', ComicsListViewSet.as_view({'post': 'list'}), name='get_manhua_comics'),
    url(r'^(?i)own-pur-coms/$', OwnPurchaseListViewSet.as_view({'post': 'post'}), name='get_own_comics'),
    url(r'^(?i)own-coll-coms/$', OwnCollectPostViewSet.as_view({'post': 'post'}), name='get_own_comics'),
    url(r'^(?i)own-coll-coms-list/$', OwnCollectListViewSet.as_view({'post': 'post'}), name='get_own_comics'),
    url(r'^(?i)search/$', SearchListViewSet.as_view({'post': 'post'}), name='get_search_comic'),
    # url(r'^own-fav-coms/$', get_own_favorite_comics, name='get_own_comics'),
    url(r'^(?i)purchase-chapter/$', PurchaseChapterViewSet.as_view({'post': 'post'})),
    url(r'^(?i)fuzzy-search/$', get_fuzzy_search_comics),
    url(r'^index-test/$', IndexComicsListViewSet.as_view({'post': 'post'}), name="get_index"),
    url(r'^index/$', get_index, name="get_index"),
    url(r'^comic-content/$', get_comics_detail, name='get_comics_detail'),
]
