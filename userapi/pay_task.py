import time
import pickle

from userapi.models import Transaction, User
from comic.celery import app
from api.helpers import r1


@app.task
def user_lock_release(email):
    # redis_obj = r1.get(email)
    # if redis_obj:
    #     user = pickle.loads(redis_obj)
    #     user.login_lock = 0
    #     ttl = r1.ttl(email)
    #     r1.setex(email, pickle.dumps(user), ttl)
    # else:
        u = User.get(email=email)
        u.login_lock = 0
        u.save()


@app.task
def order_expires(tx_id):
    t = Transaction.get(tx_id=tx_id)
    if t.status != 1:
        t.status = 2
        t.save()


@app.task
def logout(email):
    # redis_obj = r1.get(email)
    # if redis_obj:
    #     user = pickle.loads(redis_obj)
    #     # user对象active、login_lock字段置0
    #     user.active = 0
    #     user.login_lock = 0
    #     # 计算登录时长
    #     old_accumulative_time = User.get(email=email).accumulative_time
    #     old_timestamp = int(user.timestamp)
    #     now_timestamp = int("%.f" % time.time())
    #     new_accumulative_time = old_accumulative_time + now_timestamp - old_timestamp
    #     user.accumulative_time = new_accumulative_time
    #     user.save()
    #     # redis删除user对象
    #     r1.delete(email)
    # todo
    redis_obj = r1.get(email)
    if redis_obj:
        redis_obj = eval(redis_obj)
        old_timestamp = int(redis_obj.get("timestamp"))
        user = User.get(email=email)
        old_accumulative_time = int(user.accumulative_time)
        now_timestamp = int("%.f" % time.time())
        new_accumulative_time = old_accumulative_time + now_timestamp - old_timestamp
        user.accumulative_time = new_accumulative_time
        user.active = 0
        user.save()
        r1.delete(email)



