import random, string


def make_order():
    template_str = string.ascii_letters + string.digits
    tx_id = "".join([random.choice(template_str) for i in range(18)])
    return "MB" + tx_id
