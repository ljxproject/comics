import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST)
r1 = redis.Redis(host=settings.REDIS_HOST, db=1)
r5 = redis.Redis(host=settings.REDIS_HOST, db=5)
from api.helpers.myenum import EnumBase
from api.helpers.piece import attr_to_hump, hump_to_attr

from api.helpers.decorator import set_attr
from api.helpers.view_backend import MyViewBackend
