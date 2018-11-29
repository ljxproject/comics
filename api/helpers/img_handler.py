import os


def avatar_handler(filename):
    # 判断上传图片格式
    type_list = [".jpg", ".png"]
    suffix = os.path.splitext(filename)[1]
    prefix = os.path.splitext(filename)[0]
    if not suffix.lower() in type_list:
        return TypeError
    # 修改图片名字
    filename = prefix + ".png"
    # # 改变图片大小
    return filename
