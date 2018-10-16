import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST)
r1 = redis.Redis(host=settings.REDIS_HOST, db=1)
