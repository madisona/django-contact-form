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

    def test_get_message_template(self):
        class TestForm(forms.BaseEmailFormMixin):
            message_template = 'my_app/template_name.ext'
        form = TestForm()
        self.assertEqual(form.get_message_template(), {
            'template_prefix': 'my_app/',
            'template_suffix': 'ext',
            'template_name': 'template_name',
        })

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
        self.assertEqual("Cannot generate Context when form is invalid.", str(ctx.exception))

    @mock.patch("contact_form.forms.send_templated_mail", autospec=True, mocksignature=True)
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message_dict")
    def test_sends_mail_with_message_dict(self, get_message_dict, send_mock):
        mock_request = test.RequestFactory().get('/')
        get_message_dict.return_value = {"recipient_list": ["user@example.com"],
                                         "from_email": 'admin@example.com',
                                         "context": {}}

        form = forms.BaseEmailFormMixin()
        result = form.send_email(mock_request)

        send_mock.assert_called_once_with(fail_silently=False,
                                          template_suffix=mock.ANY,
                                          template_name=mock.ANY,
                                          template_prefix=mock.ANY,
                                          **get_message_dict.return_value)
        self.assertEqual(send_mock.return_value, result)

    @mock.patch("contact_form.forms.send_templated_mail", autospec=True, mocksignature=True)
    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_message_dict")
    def test_send_mail_sets_request_on_instance(self, get_message_dict, *mocks):
        mock_request = test.RequestFactory().get('/')
        get_message_dict.return_value = {"recipient_list": ["user@example.com"],
                                         "from_email": 'admin@example.com',
                                         "context": {}}

        form = forms.BaseEmailFormMixin()
        form.send_email(mock_request)
        self.assertEqual(mock_request, form.request)

    def test_get_message_dict(self):
        form = forms.BaseEmailFormMixin()
        form.is_valid = lambda: True
        form.cleaned_data = {'a': 'b'}
        form.request = mock.Mock(name='request')
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "recipient_list": form.recipient_list,
            "context": {'a': 'b', 'request': form.request},
            "headers": None
        }, message_dict)

    @mock.patch("contact_form.forms.BaseEmailFormMixin.get_context")
    def test_get_message_dict_adds_headers_when_present(self, get_context):
        email_headers = {"Reply-To": "user@example.com"}

        class HeadersForm(forms.BaseEmailFormMixin):

            def get_email_headers(self):
                return email_headers

        form = HeadersForm()
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "recipient_list": form.recipient_list,
            "context": get_context.return_value,
            "headers": email_headers,
        }, message_dict)


class ContactFormTests(test.TestCase):

    def test_is_subclass_of_form_and_base_contact_form_mixin(self):
        self.assertTrue(issubclass(forms.ContactForm, forms.BaseEmailFormMixin))
        self.assertTrue(issubclass(forms.ContactForm, forms.forms.Form))

    def test_has_valid_message_template(self):
        loader.render_to_string(forms.ContactForm.message_template)
        self.assertTrue("Message template does not exist")

    def test_sends_mail_with_headers(self):
        class ReplyToForm(forms.ContactForm):
            email = forms.forms.EmailField()

            def get_email_headers(self):
                return {'Reply-To': self.cleaned_data['email']}

        mock_request = test.RequestFactory().get('/')
        reply_to_email = u'user@example.com'  # the user's email

        form = ReplyToForm(data={'email': reply_to_email})
        message = form.send_email(mock_request)

        self.assertEqual(len(mail.outbox), 1)

        reply_to_header_email = mail.outbox[0].extra_headers['Reply-To']
        self.assertEqual(reply_to_email, reply_to_header_email)


class ContactModelFormTests(test.TestCase):

    def test_is_subclass_of_model_form_and_base_contact_form_mixin(self):
        self.assertTrue(issubclass(forms.ContactModelForm, forms.BaseEmailFormMixin))
        self.assertTrue(issubclass(forms.ContactModelForm, forms.forms.ModelForm))

    def test_has_valid_message_template(self):
        loader.render_to_string(forms.ContactModelForm.message_template)
        self.assertTrue("Message template does not exist")
