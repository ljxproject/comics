import os
import re
import subprocess

from django.conf import settings


class MangaUploadHandler(object):

    def __init__(self):
        self.sdk_path = settings.SDK_PATH
        self.sdk_env_path = settings.SDK_ENV_PATH
        self.resources_path = settings.RESOURCES_PATH

    def manga_upload(self, file):
        comics_resource_file = file
        p = subprocess.Popen("python3 %s/load_comics_resource.py %s %s" %
                             (self.sdk_path, self.sdk_env_path, comics_resource_file),
                             shell=True,
                             stderr=subprocess.PIPE, encoding='utf-8')
        res = p.stderr.readlines()
        p.communicate()
        if re.findall("error", res[-1], re.I):
            str_string = ''.join(line for line in res)
            return str_string
        else:
            return None

    def show_manga_errors(self):
        res = os.popen("python3 %s/show_errlog.py" % self.sdk_path).readlines()
        if res:
            str_string = ''.join(line for line in res)
            return str_string
        else:
            return None


mangaupload = MangaUploadHandler()
