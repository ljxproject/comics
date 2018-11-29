from api.helpers import hump_to_attr


def set_attr(func):
    def inner(instance, request):
        for k, v in request.data.items():
            if not v:
                continue
            # if v == "en":
            #     setattr(instance, hump_to_attr(k), "ms")
            #     print(getattr(instance,"lang"),"1")
            if k == "email":
                setattr(instance, hump_to_attr(k), v.lower())
            else:
                setattr(instance, hump_to_attr(k), v)
        if not hasattr(instance, "lang"):
            setattr(instance, "lang", "ms")
        else:
            if getattr(instance, "lang") == "en":
                setattr(instance, "lang", "ms")
        return func(instance, request)

    return inner
