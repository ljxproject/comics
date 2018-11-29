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

para = {"lang": "vi"}
url = "127.0.0.1:8000/comics/index-test/"
http = urllib3.PoolManager()
data = json.dumps(para).encode("utf-8")
r = http.request("POST", url, body=data, headers={"Content-Type": "application/json"})

print(r)
print(r.data)
print(r.status)
