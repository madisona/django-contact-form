
"""
Contact Form tests
"""

from django import test
from django.core.urlresolvers import reverse

from contact_form import views
from contact_form import models

class AcceptanceTestsContactPage(test.TestCase):

    def setUp(self):
        self.client = test.Client()
        self.email_data = {
            "name": "Aaron",
            "email": "aaron.l.madison@gmail.com",
            "message": "hey, I have a message",
        }

    def should_receive_200_status_code_for_contact_page(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertEqual(200, response.status_code)

    def should_use_contact_form_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertTemplateUsed(response, views.ContactPage.template_name)

    def should_have_contact_form_in_context(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertTrue(isinstance(response.context['form'], views.ContactPage.form_class), "Form isn't present or isn't correct class")

    def should_create_contact_email_object_on_successful_form_post(self):
        response = self.client.post(reverse("contact_form:contact"), self.email_data)
        contact_email = models.ContactEmail.objects.get(pk=1)
        self.assertEqual(self.email_data['name'], contact_email.name)
        self.assertEqual(self.email_data['email'], contact_email.email)
        self.assertEqual(self.email_data['message'], contact_email.message)

    def should_redirect_to_complete_page_after_successful_post(self):
        response = self.client.post(reverse("contact_form:contact"), self.email_data)
        self.assertRedirects(response, reverse("contact_form:completed"))

class AcceptanceTestsContactCompletedPage(test.TestCase):

    def should_receive_200_status_code_for_completed_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertEqual(200, response.status_code)

    def should_use_completed_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertTemplateUsed(response, views.CompletedPage.template_name)
