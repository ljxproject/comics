import os

if os.environ.get('DJANGO_PRODUCTION_SETTINGS', None):
    from .pro_settings import *
else:
    from .dev_settings import *
