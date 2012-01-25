from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, FormView

from forms import ContactForm

class CompletedPage(TemplateView):
    template_name = "contact_form/contact_completed.html"

class ContactFormMixin(object):
    """
    Form view that sends email when form is valid. You'll need
    to define your own form_class and template_name.
    """
    def form_valid(self, form):
        form.send_email(self.request)
        return super(ContactFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse("contact_form:completed")

class ContactFormView(ContactFormMixin, FormView):
    form_class = ContactForm
    template_name = "contact_form/contact.html"

    def get_form_kwargs(self):
        "We use user in the form to autocomplete some fields"
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ContactModelFormView(ContactFormMixin, CreateView):
    pass
