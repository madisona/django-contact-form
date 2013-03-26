from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from templated_email import send_templated_mail


class BaseEmailFormMixin(object):
    from_email = settings.DEFAULT_FROM_EMAIL
    message_template = 'contact_form/email/contact_form_reply.html'
    recipient_list = [email for _, email in settings.MANAGERS]

    def get_message_template(self):
        ext = self.message_template.split('.')[-1]
        parts = self.message_template.split('/')
        template_prefix = self.message_template.replace(parts[-1], '')
        template_name = parts[-1].replace(ext, '')[:-1]
        return {
            'template_prefix': template_prefix,
            'template_suffix': ext,
            'template_name': template_name,
        }

    def get_context(self):
        """
        Context sent to templates for rendering include the form's cleaned
        data and also the current Request object.
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context when form is invalid.")
        return dict(request=self.request, **self.cleaned_data)

    def get_email_headers(self):
        """
        Subclasses can replace this method to define additional settings like
        a reply_to value.
        """
        return None

    def get_recipient_list(self):
        return self.recipient_list

    def get_message_dict(self):
        return {
            "from_email": self.from_email,
            "recipient_list": self.get_recipient_list(),
            "context": self.get_context(),
            "headers": self.get_email_headers(),
        }

    def send_email(self, request, fail_silently=False):
        self.request = request
        kwargs = self.get_message_template()
        kwargs.update(self.get_message_dict())
        return send_templated_mail(fail_silently=fail_silently, **kwargs)


class ContactForm(forms.Form, BaseEmailFormMixin):
    """
    Subclass this and declare your own fields.
    """


class ContactModelForm(forms.ModelForm, BaseEmailFormMixin):
    """
    You'll need to declare the model yourself.
    """


class BasicContactForm(ContactForm):
    """
    A very basic contact form you can use out of the box if you wish.
    """
    name = forms.CharField(label=_(u'Your name'), max_length=100)
    email = forms.EmailField(label=_(u'Your email address'), max_length=200)
    body = forms.CharField(label=_(u'Your message'), widget=forms.Textarea())

    def get_email_headers(self):
        return {'Reply-To': self.cleaned_data['email']}
