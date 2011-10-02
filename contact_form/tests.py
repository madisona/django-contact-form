
"""
Contact Form tests
"""
from mock import patch, Mock

from django import test
from django.core.urlresolvers import reverse
from django.template import loader, TemplateDoesNotExist

from contact_form import views
from contact_form import models
from contact_form import forms

class AcceptanceTestsContactPage(test.TestCase):

    def setUp(self):
        self.client = test.Client()
        self.email_data = {
            "name": "Aaron",
            "email": "aaron.l.madison@gmail.com",
            "message": "hey, I have a message",
        }

    def test_receives_200_status_code_for_contact_page(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertEqual(200, response.status_code)

    def test_uses_contact_form_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertTemplateUsed(response, views.ContactPage.template_name)

    def test_has_contact_form_in_context(self):
        response = self.client.get(reverse("contact_form:contact"))
        self.assertTrue(isinstance(response.context['form'], views.ContactPage.form_class), "Form isn't present or isn't correct class")

    @patch("contact_form.forms.ContactForm.send_email", Mock())
    def test_creates_contact_email_object_on_successful_form_post(self):
        response = self.client.post(reverse("contact_form:contact"), self.email_data)
        contact_email = models.ContactEmail.objects.get(pk=1)
        self.assertEqual(self.email_data['name'], contact_email.name)
        self.assertEqual(self.email_data['email'], contact_email.email)
        self.assertEqual(self.email_data['message'], contact_email.message)

    @patch("contact_form.forms.ContactForm.send_email")
    def test_sends_email_on_successful_form_post(self, send_email):
        self.client.post(reverse("contact_form:contact"), self.email_data)
        self.assertTrue(send_email.called, "Didn't send email on successful post")

    @patch("contact_form.forms.ContactForm.send_email", Mock())
    def test_redirects_to_complete_page_after_successful_post(self):
        response = self.client.post(reverse("contact_form:contact"), self.email_data)
        self.assertRedirects(response, reverse("contact_form:completed"))

class AcceptanceTestsContactCompletedPage(test.TestCase):

    def test_receives_200_status_code_for_completed_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertEqual(200, response.status_code)

    def test_uses_completed_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertTemplateUsed(response, views.CompletedPage.template_name)

class ContactFormTests(test.TestCase):

    @patch("contact_form.forms.ContactForm.get_context", Mock())
    @patch("django.template.loader.render_to_string")
    def test_renders_email_template_to_string(self, render_to_string):
        form = forms.ContactForm()
        message = form.get_message()
        self.assertEqual([(form.template_name, form.get_context()), {}], render_to_string.call_args)
        self.assertEqual(render_to_string.return_value, message)

    @patch("contact_form.forms.ContactForm.get_context", Mock())
    @patch("django.template.loader.render_to_string")
    def test_renders_subject_template_to_string(self, render_to_string):
        render_to_string.return_value = "User has contacted you"
        form = forms.ContactForm()
        subject = form.get_subject()
        self.assertEqual([(form.subject_template_name, form.get_context()), {}], render_to_string.call_args)
        self.assertEqual(render_to_string.return_value, subject)

    @patch("contact_form.forms.ContactForm.get_context", Mock())
    @patch("django.template.loader.render_to_string")
    def test_forces_subject_to_be_one_line(self, render_to_string):
        render_to_string.return_value = "User has \ncontacted you\n"
        form = forms.ContactForm()
        subject = form.get_subject()
        self.assertEqual("User has contacted you", subject)

    @patch("contact_form.forms.ContactForm.is_valid", Mock(return_value=False))
    def test_receives_valid_error_if_form_is_invalid(self):
        form = forms.ContactForm()
        self.assertRaises(ValueError, form.get_context)

    @patch("contact_form.forms.ContactForm.is_valid", Mock(return_value=True))
    @patch("django.contrib.sites.models.Site.objects.get_current")
    @patch("contact_form.forms.RequestContext")
    def test_returns_request_context_if_form_is_valid(self, request_context, current_site):
        form = forms.ContactForm()
        form.request = Mock()
        form.cleaned_data = {'name': 'aaron'}

        context = form.get_context()
        self.assertEqual(request_context.return_value, context)
        self.assertEqual([(form.request, {
            'name': 'aaron',
            'site': current_site.return_value,
        }), {}], request_context.call_args)

    @patch("contact_form.forms.send_mail")
    @patch("contact_form.forms.ContactForm.get_message_dict")
    def test_sends_mail_with_message_dict(self, get_message_dict, send_mail):
        get_message_dict.return_value = {"name": "aaron"}
        form = forms.ContactForm()
        form.send_email(Mock())

        self.assertEqual([(), dict(get_message_dict.return_value, fail_silently=False)] , send_mail.call_args)

    @patch("contact_form.forms.ContactForm.get_subject")
    @patch("contact_form.forms.ContactForm.get_message")
    def test_gets_message_dict(self, get_message, get_subject):
        form = forms.ContactForm()
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "recipient_list": form.recipient_list,
            "message": get_message.return_value,
            "subject": get_subject.return_value,
        }, message_dict)

    def test_has_valid_subject_template(self):
        template_exists = 1
        try:
            loader.render_to_string(forms.ContactForm.subject_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Subject template does not exist")

    def test_has_valid_message_template(self):
        template_exists = 1
        try:
            loader.render_to_string(forms.ContactForm.template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Email message template does not exist")