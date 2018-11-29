class EnumBase(object):
    code_dict = {}
    category_dict = {}
    comic_dict = {}

    @staticmethod
    def _get_name():
        pass

    @classmethod
    def set_d(cls):
        for i in cls.__subclasses__():
            tp, lang = cls.get_dict(i)
            if tp == "code":
                cls.code_dict[lang] = i
            elif tp == "category":
                cls.category_dict[lang] = i
            elif tp == "comic":
                cls.comic_dict[lang] = i

    @classmethod
    def get_status_obj(cls, o, name):
        obj = getattr(o, name)
        return obj

    @classmethod
    def get_dict(cls, o):
        name = o._get_name()
        return tuple(name.split("_"))



    @classmethod
    def get_status(cls, i, o, lang="en"):
        value = i
        name = o.get_name_from_value(i)
        tp = cls.get_dict(o)[0]
        dic = getattr(EnumBase, "%s_dict" % tp)
        if lang not in dic or lang == "en":
            name = cls.get_status_default_name(i, o)
        else:
            obj = dic[lang]
            obj = cls.get_status_obj(obj, name)
            name = obj.value.replace("_", " ").title()
        status = {
            "status": value,
            "msg": name
        }
        return status

    @classmethod
    def get_status_default_name(cls, i, o):
        """
        :param i: the value(int) of attr in class
        :param o:the class of model in api.helpers.code.en.py eg:CategoryEN
        :return: key map by value in class
        """
        name = o.get_name_from_value(i).replace("_", " ").title()
        return name

    @classmethod
    def get_model_status(cls, o1, o2):
        """
        :param o1: default class eg:CategoryEn
        :param o2: the class of model in api.helpers.code.zh.py eg:CategoryZh
        :return: the element of tuple contain key and value by tuple
        eg: ((key1,value1,),(key2,value2,),...)
        """
        return tuple((k, v) for k, v in {o1[k].value: v.value for k, v in o2.__members__.items()}.items())
