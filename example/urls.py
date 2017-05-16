from django.conf.urls import include, url


from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^contact/', include("contact_form.urls", namespace="contact_form")),
    url(r'^admin/', include(admin.site.urls)),
]
