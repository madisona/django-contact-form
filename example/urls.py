
from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^contact/', include('contact_form.urls', namespace='contact_form')),
    url(r'^admin/', admin.site.urls),
]
