from django.conf.urls import url
from api.views import get_comics_info, get_index, get_edit_comics,\
    get_trend_comics, get_own_purchase_comics, get_finish_comics,\
    get_own_favorite_comics, get_comics_detail, get_search_comics,\
    PurchaseChapterViewSet, get_fuzzy_search_comics, get_manga_comics, \
    get_manhua_comics

urlpatterns = [
    url(r'^(?P<com_id>\d+)/$', get_comics_info, name='get_comics_info'),
    url(r'^(?i)editor-recommend/$', get_edit_comics, name='get_edit_comics'),
    url(r'^(?i)finish-recommend/$', get_finish_comics, name='get_finish_comics'),
    url(r'^(?i)trend-recommend/$', get_trend_comics, name='get_trend_comics'),
    url(r'^(?i)manga/$', get_manga_comics, name='get_manga_comics'),
    url(r'^(?i)manhua/$', get_manhua_comics, name='get_finish_comics'),
    url(r'^(?i)own-pur-coms/$', get_own_purchase_comics, name='get_own_comics'),
    url(r'^(?i)search/$', get_search_comics, name='get_search_comic'),
    # url(r'^own-fav-coms/$', get_own_favorite_comics, name='get_own_comics'),
    url(r'^(?i)pur-chaps/$', PurchaseChapterViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^(?P<com_id>\d+)/(?P<chap_id>\d+)/$', get_comics_detail, name='get_comics_detail'),
    url(r'^(?i)fuzzy-search/$', get_fuzzy_search_comics),
    url(r'^$', get_index, name="get_index")
]
