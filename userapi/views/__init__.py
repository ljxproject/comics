from userapi.views.register_and_login import UsersLogin, UsersLogout, UsersSendCode
from userapi.views.user_detail import UserDetail
from userapi.views.perfection import ChangeEmailViewSet, ChangeGenderViewSet, ChangeAvatarViewSet, ChangeNameViewSet, \
    ChangeWalletViewSet, CreateOderViewSet
from userapi.views.feedback import FeedBackDetailClientViewSet, feedback_detail_return, feedback_award
from userapi.views.comment import CommentListViewSet, CommentUpdateViewSet