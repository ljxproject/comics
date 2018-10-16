
class Model(object):

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.objects.get(*args, **kwargs)

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def values_list(cls, *args, **kwargs):
        return cls.objects.values_list(*args, **kwargs)