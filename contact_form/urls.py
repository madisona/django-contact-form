
from django.conf.urls.defaults import *

from contact_form.views import ContactFormView, CompletedPage

urlpatterns = patterns('',
    url(r'^completed/$', CompletedPage.as_view(), name="completed"),
    url(r'^$', ContactFormView.as_view(), name="form"),
)
