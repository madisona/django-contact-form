
import django
import debug_toolbar

if django.get_version() >= '2.0.0':
    from django.urls import re_path as url
    from django.urls import include
else:
    from django.conf.urls import url, include

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^contact/', include('contact_form.urls', namespace='contact_form')),
    url(r'^admin/', admin.site.urls),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
