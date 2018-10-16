from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer
from userapi.models import User, PurchaseAndFavorite


@api_view(["GET"])
def user_detail(request, email):
    """
    用户详细信息
    接收email
    """
    # 登录后查询用户信息表
    user = User.get(email=email)
    name = user.name
    if user.avatar:
        avatar = str(user.avatar)
    else:
        avatar = ''
    if user.gender == None:
        gender = ''
    else:
        gender = user.gender
    if user.wallet_ios or user.wallet_android:
        system = request.GET.get("system")
        if system == "ios":
            wallet = user.wallet_ios
        elif system == "android":
            wallet = user.wallet_android
    else:
        wallet = ''
    purchased_amount = PurchaseAndFavorite.filter(email=email, status=1).count()
    data = ComicMethod.pack_user_data(name=name, avatar=avatar, wallet=wallet,
                                      gender=str(gender), purchased_amount=str(purchased_amount))

    serializer = ComicsSuccessSerializer(data)
    return Response(serializer.data)
