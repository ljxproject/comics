"""comic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # url(r'^docs/', include_docs_urls(title="漫画项目接口文档")),
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^comics/', include('api.urls')),
    url(r'^users/', include('userapi.urls', namespace='userapi')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^adminx/', include('adminx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = "api.views.page_not_found"
# handler500 = "api.views.page_error"


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
