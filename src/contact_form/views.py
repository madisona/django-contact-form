
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView

from contact_form.forms import ContactForm

class CompletedPage(TemplateView):
    template_name = "contact_form/contact_completed.html"

class ContactPage(CreateView):
    template_name = "contact_form/contact.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse("contact_form:completed")