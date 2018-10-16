from django.conf.urls import url
from adminx.views import check_progress

urlpatterns = [
    url(r'check_progress$', check_progress, name="check_progress$"),

]
