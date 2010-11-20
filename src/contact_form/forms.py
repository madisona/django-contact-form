
from django import forms

from contact_form import models

class ContactForm(forms.ModelForm):

    class Meta:
        model = models.ContactData 