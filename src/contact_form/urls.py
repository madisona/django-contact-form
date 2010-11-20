
from django.conf.urls.defaults import *

from contact_form.views import ContactPage

urlpatterns = patterns('',
    url(r'^$', ContactPage.as_view(), name="index"),
    url(r'^completed/$', "contact_form.views.completed", name="completed"),
)