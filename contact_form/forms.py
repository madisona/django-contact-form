
from django import forms
from django.conf import settings
from django.forms.widgets import Textarea
from django.template import loader
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class BaseEmailFormMixin(object):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email for _, email in settings.MANAGERS]

    subject_template_name = 'contact_form/email_subject.txt'
    message_template_name = 'contact_form/email_template.txt'

    def get_message(self):
        return loader.render_to_string(self.message_template_name, self.get_context())

    def get_subject(self):
        subject = loader.render_to_string(self.subject_template_name, self.get_context())
        return ''.join(subject.splitlines())

    def get_context(self):
        if not self.is_valid():
            raise ValueError("Cannot generate Context when form is invalid.")
        return self.cleaned_data

    def get_message_dict(self):
        return {
            "from_email": self.from_email,
            "recipient_list": self.recipient_list,
            "subject": self.get_subject(),
            "message": self.get_message(),
        }

    def send_email(self, request, fail_silently=False):
        self.request = request
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


class ContactForm(forms.Form, BaseEmailFormMixin):
    name = forms.CharField()
    email = forms.EmailField(help_text=_('A valid email address, please.'))
    phone = forms.CharField(required=False)
    subject = forms.CharField(max_length=100,
        help_text=_('100 characters max.'))
    message = forms.CharField(widget=Textarea)
    cc_myself = forms.BooleanField(required=False)

    def __init__(self, user=None, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["email"].initial = user.email
            self.fields["name"].initial = user.get_full_name()


class ContactModelForm(forms.ModelForm, BaseEmailFormMixin):
    """
    You'll need to declare the model yourself.
    """
    pass
