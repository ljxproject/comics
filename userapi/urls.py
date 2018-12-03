from django.conf.urls import url
from userapi.views import UserDetail, ChangeGenderViewSet, \
    ChangeNameViewSet, ChangeAvatarViewSet, ChangeWalletViewSet, ChangeEmailViewSet, \
    CreateOderViewSet, FeedBackDetailClientViewSet, \
    feedback_detail_return, feedback_award, UsersLogout, UsersSendCode, UsersLogin, \
    CommentUpdateViewSet, CommentListViewSet

urlpatterns = [
    url(r'^register-login/$', UsersLogin.as_view({'post': "post"}), name='register_and_login'),
    url(r'^logout/$', UsersLogout.as_view({'post': "post"}), name='logout'),
    url(r'^me/$', UserDetail.as_view({'post': 'post'}), name='user_detail'),
    url(r'^perfection/email/$', ChangeEmailViewSet.as_view({'post': 'post'})),
    url(r'^perfection/name/$', ChangeNameViewSet.as_view({'post': 'post'})),
    url(r'^perfection/avatar/$', ChangeAvatarViewSet.as_view({'post': 'post'})),
    url(r'^top-up-2/$', ChangeWalletViewSet.as_view({'post': 'post'})),
    url(r'^top-up/$', CreateOderViewSet.as_view({'post': 'post'})),
    url(r'^perfection/gender/$', ChangeGenderViewSet.as_view({'post': 'post'})),
    url(r'^send-code/$', UsersSendCode.as_view({'post': "post"}), name='send_register_code'),
    # url(r'^check-session/$', check_session, name='send_session_id'),
    url(r'^feedback/client/$', FeedBackDetailClientViewSet.as_view({'post': 'post'}), name="fbd"),
    url(r'^feedback/server/(?P<fbd_id>\d+)/$', feedback_award, name='fba'),
    # url(r'^controller/$', UsersController.as_view({'post': "post"}), name='fba'),
    # url(r'^perfection/$', UserBaseInfo.as_view({'post': "post"}), name='fba'),
    url(r'^comment/list/$', CommentListViewSet.as_view({'post': "post"})),
    url(r'^comment/release/$', CommentUpdateViewSet.as_view({'post': "post"})),

    url(r'^feedback/c-r/$', feedback_detail_return, name='fbdr'),
    url(r'^feedback/c-r/$', feedback_detail_return, name='fbdr'),
]
