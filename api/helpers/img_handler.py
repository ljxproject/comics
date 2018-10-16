import os



from api.helpers.code import Code


def avatar_handler(filename):
    # 判断上传图片格式
    type_list = [".jpg", ".png"]
    suffix = os.path.splitext(filename)[1]
    prefix = os.path.splitext(filename)[0]
    if not suffix.lower() in type_list:
        data = {
            "status": Code.invalied_image.value,
            "msg": Code.invalied_image.name.replace("_", " ").title(),
        }
        return data
    # 修改图片名字
    filename = prefix + ".png"
    # # 改变图片大小
    # avatar.thumbnail((300, 300))
    return filename
