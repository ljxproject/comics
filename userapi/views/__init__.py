from userapi.views.register_and_login import register_and_login, logout, send_code, \
    check_session
from userapi.views.user_detail import user_detail
from userapi.views.perfection import ChangeEmailViewSet, ChangeGenderViewSet, ChangeAvatarViewSet, ChangeNameViewSet, \
    ChangeWalletViewSet, CreateOderViewSet
from userapi.views.feedback import FeedBackDetailClientViewSet, feedback_detail_return, feedback_award
