from api.views.view_listbase import ComicsListBaseView
from api.views.comics_info import ComicInfoViewSet, ChapterInfoViewSet
from api.views.index import IndexComicsListViewSet
from api.views.index import get_index
from api.views.comics_detail import get_comics_detail
from api.views.purchase_chapter import PurchaseChapterViewSet
from api.views.fuzzy_search import get_fuzzy_search_comics

from api.views.comics_list import ComicsListViewSet, SearchListViewSet, OwnPurchaseListViewSet, OwnCollectPostViewSet, \
    OwnCollectListViewSet
from api.views.error_view import page_not_found, page_error
