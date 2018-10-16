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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comic.settings")  # project_name 项目名称
# #
django.setup()

# import datetime
import sys
from datetime import datetime
import shutil

import uuid
a = str(uuid.uuid4()).split("-")[1]
print(a)