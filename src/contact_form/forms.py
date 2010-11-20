
from django import forms
from django.core.mail import send_mail

from contact_form import models

class ContactForm(forms.ModelForm):

    class Meta:
        model = models.ContactEmail

    def save(self, *args, **kwargs):
        print("send the email sucka!")
        return super(ContactForm, self).save(*args, **kwargs)