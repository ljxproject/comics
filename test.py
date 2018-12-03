# # -*- coding: utf-8 -*-
import os
# #
# import time
#
import time

import django

# import pytz
# from django.utils import timezone
# #
# from comic import settings
from django.http import HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comic.dev_settings")  # project_name 项目名称
# #
django.setup()

import json
import urllib3
import threading


def send(*args):
    # print(args[0])
    # para = {"lang": "vi", "k": args[0]}
    url = "http://ip.taobao.com/service/getIpInfo.php"
    http = urllib3.PoolManager()
    # data = json.dumps(para).encode("utf-8")
    # http.request("POST", url, body=data, headers={"Content-Type": "application/json"})
    r = http.request("GET", url, fields={"ip": "65.49.71.112"}, retries=3, timeout=2)
    print(json.loads(r.data, encoding="utf-8"), r.status)


if __name__ == '__main__':
    # l = []
    # for i in range(10):
    #     s = threading.Thread(target=send, args=(i,))
    #     l.append(s)
    #     s.start()
    #     print("send")
    # for p in l:
    #     p.join()
    #     print("end")
    send(0)
