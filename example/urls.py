from django.conf.urls.defaults import patterns, include, url


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^contact/', include("contact_form.urls", namespace="contact_form")),
    url(r'^admin/', include(admin.site.urls)),
)
