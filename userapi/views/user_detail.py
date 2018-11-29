from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import set_attr, MyViewBackend
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from userapi.models import PurchaseAndFavorite


class UserDetail(viewsets.ViewSet, MyViewBackend):

    @set_attr
    def post(self, request):
        if hasattr(self, "email"):
            data = self._pre_check()
            if not isinstance(data, dict):
                data = self.get_user_detail(user=data)
        else:
            data = self.get_user_detail()
        serializer = ComicsSuccessSerializer(data)
        return Response(serializer.data)

    def get_user_detail(self, user=None):
        if user:
            system = getattr(self, "app_key")
            email = user.email
            name = user.name
            avatar = str(user.avatar)
            if system == "ios":
                wallet = user.wallet_ios
            else:
                wallet = user.wallet_android
            gender = user.gender
            purchased_amount = PurchaseAndFavorite.filter(email=email, status=1).count()
        else:
            name = ''
            avatar = ''
            gender = ''
            wallet = ''
            purchased_amount = 0
        data = ComicMethod.pack_success_data(user_name=name, user_avatar=avatar, user_wallet=wallet,
                                             user_gender=str(gender), purchased_amount=str(purchased_amount))
        return data
