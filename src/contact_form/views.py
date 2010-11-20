
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

from contact_form.forms import ContactForm


def completed(request):
    from django import http
    return http.HttpResponse("completed")

class ContactPage(CreateView):
    template_name = "contact_form/contact_form.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse("contact_form:completed")