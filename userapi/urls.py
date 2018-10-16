from django.conf.urls import url
from userapi.views import register_and_login, logout, user_detail, ChangeGenderViewSet, \
    ChangeNameViewSet, ChangeAvatarViewSet, ChangeWalletViewSet, ChangeEmailViewSet, \
    send_code, check_session, CreateOderViewSet, FeedBackDetailClientViewSet, \
    feedback_detail_return, feedback_award

urlpatterns = [
    url(r'^register-login/$', register_and_login, name='register_and_login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^(?P<email>.+@.+)/$', user_detail, name='user_detail'),
    # url(r'^perfection/email/$', ChangeEmailViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^perfection/name/$', ChangeNameViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^perfection/avatar/$', ChangeAvatarViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^top-up-2/$', ChangeWalletViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^top-up/$', CreateOderViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^perfection/gender/$', ChangeGenderViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url(r'^send-code/$', send_code, name='send_register_code'),
    url(r'^check-session/$', check_session, name='send_session_id'),
    url(r'^feedback/client/$', FeedBackDetailClientViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name="fbd"),
    url(r'^feedback/server/(?P<fbd_id>\d+)/$', feedback_award, name='fba'),

    url(r'^feedback/c-r', feedback_detail_return, name='fbdr')
]
