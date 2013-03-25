"""
Contact Form tests
"""
import mock

from django import test
from django.core import mail
from django.core.urlresolvers import reverse
from django.template import loader, TemplateDoesNotExist

from contact_form import forms, views



class AcceptanceTestsContactCompletedPage(test.TestCase):

    def test_receives_200_status_code_for_completed_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertEqual(200, response.status_code)

    def test_uses_completed_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertTemplateUsed(response, views.CompletedPage.template_name)


class BaseEmailFormMixinTests(test.TestCase):

    @mock.patch('django.template.loader.render_to_string')
    def test_get_message_returns_rendered_message_template(self, render_to_string):
        context = {'message': 'an example message.'}

        class TestForm(forms.BaseEmailFormMixin):
            message_template_name = "my_template.html"
            def get_context(self):
                return context

        form = TestForm()

        message = form.get_message()
        self.assertEqual(render_to_string.return_value, message)
        render_to_string.assert_called_once_with(form.message_template_name, context)

    @mock.patch('django.template.loader.render_to_string')
    def test_get_subject_returns_single_line_rendered_subject_template(self, render_to_string):
        render_to_string.return_value = 'This is \na \ntemplate.'
        context = {'message': 'an example message.'}

        class TestForm(forms.BaseEmailFormMixin):
            subject_template_name = "my_template.html"
            def get_context(self):
                return context

        form = TestForm()

        subject = form.get_subject()
        self.assertEqual('This is a template.', subject)
        render_to_string.assert_called_once_with(form.subject_template_name, context)

    def test_get_context_returns_cleaned_data_with_request_when_form_is_valid(self):
        request = test.RequestFactory().post("/")
        class TestForm(forms.BaseEmailFormMixin, forms.forms.Form):
            name = forms.forms.CharField()

        form = TestForm(data={'name': 'test'})
        form.request = request
        self.assertEqual(dict(name='test', request=request), form.get_context())

    def test_get_context_returns_value_error_when_form_is_invalid(self):
        class TestForm(forms.BaseEmailFormMixin, forms.forms.Form):
            name = forms.forms.CharField()

        form = TestForm(data={})
        with self.assertRaises(ValueError) as ctx:
            form.get_context()
        self.assertEqual("Cannot generate Context when form is invalid.", ctx.exception.message)

    @mock.patch("contact_form.forms.EmailMessage", autospec=True, mocksignature=True)
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message_dict")
    def test_sends_mail_with_message_dict(self, get_message_dict, email_class):
        mock_request = test.RequestFactory().get('/')
        get_message_dict.return_value = {"to": ["user@example.com"]}

        form = forms.BaseEmailFormMixin()
        result = form.send_email(mock_request)

        email_class.assert_called_once_with(**get_message_dict.return_value)
        email_class.return_value.send.assert_called_once_with(fail_silently=False)
        self.assertEqual(email_class.return_value.send.return_value, result)

    @mock.patch("contact_form.forms.EmailMessage", autospec=True, mocksignature=True)
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message_dict")
    def test_send_mail_sets_request_on_instance(self, get_message_dict, *mocks):
        mock_request = test.RequestFactory().get('/')
        get_message_dict.return_value = {"to": ["user@example.com"]}

        form = forms.BaseEmailFormMixin()
        form.send_email(mock_request)
        self.assertEqual(mock_request, form.request)

    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_subject")
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message")
    def test_gets_message_dict(self, get_message, get_subject):
        form = forms.BaseEmailFormMixin()
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "to": form.recipient_list,
            "body": get_message.return_value,
            "subject": get_subject.return_value,
        }, message_dict)

    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_subject")
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message")
    def test_get_message_dict_adds_headers_when_present(self, get_message, get_subject):
        email_headers = {"Reply-To": "user@example.com"}

        class HeadersForm(forms.BaseEmailFormMixin):

            def get_email_headers(self):
                return email_headers

        form = HeadersForm()
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "to": form.recipient_list,
            "body": get_message.return_value,
            "subject": get_subject.return_value,
            "headers": email_headers,
        }, message_dict)


class ContactFormTests(test.TestCase):

    def test_is_subclass_of_form_and_base_contact_form_mixin(self):
        self.assertTrue(issubclass(forms.ContactForm, forms.BaseEmailFormMixin))
        self.assertTrue(issubclass(forms.ContactForm, forms.forms.Form))

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
            loader.render_to_string(forms.ContactForm.message_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Email message template does not exist")

    def test_sends_mail_with_headers(self):
        class ReplyToForm(forms.ContactForm):
            email = forms.forms.EmailField()

            def get_email_headers(self):
                return {'Reply-To': self.cleaned_data['email']}

        mock_request = test.RequestFactory().get('/')
        reply_to_email = u'user@example.com'  # the user's email

        form = ReplyToForm(data={'email': reply_to_email})
        message = form.send_email(mock_request)

        reply_to_header_email = mail.outbox[0].extra_headers['Reply-To']
        self.assertEqual(reply_to_email, reply_to_header_email)


class ContactModelFormTests(test.TestCase):

    def test_is_subclass_of_model_form_and_base_contact_form_mixin(self):
        self.assertTrue(issubclass(forms.ContactModelForm, forms.BaseEmailFormMixin))
        self.assertTrue(issubclass(forms.ContactModelForm, forms.forms.ModelForm))

    def test_has_valid_subject_template(self):
        template_exists = 1
        try:
            loader.render_to_string(forms.ContactModelForm.subject_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Subject template does not exist")

    def test_has_valid_message_template(self):
        template_exists = 1
        try:
            loader.render_to_string(forms.ContactModelForm.message_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Email message template does not exist")
