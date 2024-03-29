import django

if django.get_version() >= '2.0.0':
    from django.urls import re_path as url
else:
    from django.conf.urls import url

from contact_form import views, forms

app_name = 'contact_form'
urlpatterns = [
    url(r'^$', views.ContactFormView.as_view(
        template_name="contact_form/contact.html",
        form_class=forms.BasicContactForm,
    ), name="contact"),
    url(r'^completed/$', views.CompletedPage.as_view(), name="completed"),
]
