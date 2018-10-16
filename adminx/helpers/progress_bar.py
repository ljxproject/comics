from api.helpers import r


class ProgressBar(object):

    def write(self, key, value, time=None):
        if key:
            r.setex(key, [value, time], 60)

    def read(self, key):
        re = r.get(key)
        return re


p_b = ProgressBar()
