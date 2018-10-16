from rest_framework import viewsets
from rest_framework.response import Response

from api.helpers import r1, r
from api.helpers.code import Code
from api.helpers.comic_method import ComicMethod
from api.helpers.serializer import ComicsSuccessSerializer, PurchaseChapterSerializer
from api.models import ComicInfo
from userapi.models import User, PurchaseAndFavorite


class PurchaseChapterViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseChapterSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(request.data)

    def update(self, request, *args, **kwargs):
        system = request.data.get("system")
        form = PurchaseChapterSerializer(data=request.data)
        if form.is_valid():
            email = form.data.get("email")
            com_id = form.data.get("com_id")
            chap_id = form.data.get("chap_id")
            key = request.session.session_key
            # 是否已登录
            if key:
                values = r1.get(email)
                # 是否是最新机器
                if values and key == values.decode(encoding='utf-8'):
                    # 该章节是否免费
                    com = ComicInfo.get(com_id=com_id)
                    chap_id_list_free = [str(i + 1) for i in range(com.free_chapter)]
                    if chap_id in chap_id_list_free:
                        data = {
                            "status": Code.this_chapter_has_been_freed.value,
                            "msg": Code.this_chapter_has_been_freed.name.replace("_", " ").title(),
                        }
                        serializer = ComicsSuccessSerializer(data)
                        return Response(serializer.data)
                    # 该章节是否超出上限
                    if int(chap_id) > int(com.total_chapter):
                        data = {
                            "status": Code.chapter_not_found.value,
                            "msg": Code.chapter_not_found.name.replace("_", " ").title(),
                        }
                        serializer = ComicsSuccessSerializer(data)
                        return Response(serializer.data)
                    # 该用户是否已购买此书
                    obj = PurchaseAndFavorite.filter(email=email, com_id=com_id)
                    if not obj:
                        PurchaseAndFavorite(email=email, com_id=com_id, status=0).save()
                    # 调取本章节价格
                    img_re = ComicMethod.get_one_img_resource(com_id=com_id, chap_id=chap_id)
                    price = img_re[0]["price"]
                    # 扣除价格
                    user = User.get(email=email)
                    if system == "ios":
                        wallet_obj = float(user.wallet_ios)
                        wallet = '%.2f' % float(wallet_obj - float(price))
                        if wallet >= "0":
                            user.wallet_ios = wallet
                            user.save()
                        else:
                            data = {
                                "status": Code.insufficient_fund.value,
                                "msg": Code.insufficient_fund.name.replace("_", " ").title(),
                            }
                            serializer = ComicsSuccessSerializer(data)
                            return Response(serializer.data)
                    elif system == "android":
                        wallet_obj = float(user.wallet_android)
                        wallet = '%.2f' % float(wallet_obj - float(price))
                        if wallet >= "0":
                            user.wallet_android = wallet
                            user.save()
                        else:
                            data = {
                                "status": Code.insufficient_fund.value,
                                "msg": Code.insufficient_fund.name.replace("_", " ").title(),
                            }
                            serializer = ComicsSuccessSerializer(data)
                            return Response(serializer.data)

                    # 存进redis权限表
                    permission_re = ComicMethod.get_user_chapter_authority(email=email, com_id=com_id)
                    chap_id_list = eval(permission_re) if isinstance(permission_re, bytes) else permission_re
                    # 判断redis是否已有该章节
                    if chap_id in chap_id_list:
                        data = {
                            "status": Code.this_chapter_has_been_purchased.value,
                            "msg": Code.this_chapter_has_been_purchased.name.replace("_", " ").title(),
                        }
                        serializer = ComicsSuccessSerializer(data)
                        return Response(serializer.data)
                    chap_id_list.append(str(chap_id))
                    r.hset("%s_authority" % email, "%s" % com_id, chap_id_list)
                    r.expire("%s_authority" % email, 24 * 60 * 60)  # todo 过期时间 24*60*60(一天)
                    com.increase_download()
                    data = ComicMethod.pack_success_data()
                    serializer = ComicsSuccessSerializer(data)
                    return Response(serializer.data)
            data = {
                "status": Code.you_are_offline_in_this_device.value,
                "msg": Code.you_are_offline_in_this_device.name.replace("_", " ").title(),
            }
            serializer = ComicsSuccessSerializer(data)
            return Response(serializer.data)
        else:
            return Response(request.data)

