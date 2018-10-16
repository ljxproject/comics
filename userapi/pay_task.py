from userapi.models import Transaction
from comic.celery import app
from userapi.models import User


@app.task
def user_lock_release(email):
    u = User.get(email=email)
    if u.login_lock == 1:
        u.login_lock = 0
        u.save()


@app.task
def order_expires(tx_id):
    t = Transaction.get(tx_id=tx_id)
    if t.status != 1:
        t.status = 2
        t.save()


@app.task
def active_to_inactive(obj):
    if obj.active == 1:
        obj.active = 0
        obj.save()
