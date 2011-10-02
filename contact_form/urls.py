
from django.conf.urls.defaults import *

from contact_form import views

urlpatterns = patterns('',
    url(r'^completed/$', views.CompletedPage.as_view(), name="completed"),
)