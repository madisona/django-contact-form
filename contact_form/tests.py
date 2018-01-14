"""
Contact Form tests
"""
import mock

from django import test
from django.core import mail
from django.urls import reverse
from django.template import loader, TemplateDoesNotExist
from django import forms as django_forms

from contact_form import forms, views


class AcceptanceTestsContactCompletedPage(test.TestCase):
    def test_receives_200_status_code_for_completed_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertEqual(200, response.status_code)

    def test_uses_completed_template_when_rendering_page(self):
        response = self.client.get(reverse("contact_form:completed"))
        self.assertTemplateUsed(response, views.CompletedPage.template_name)


class SampleBasicTestForm(forms.BaseEmailFormMixin, django_forms.Form):
    field = django_forms.CharField()


class SampleCustomizedTestForm(forms.BaseEmailFormMixin, django_forms.Form):
    field = django_forms.CharField()

    def get_subject(self):
        return "My Subject"

    def get_bcc(self):
        return ["bcc@example.com"]

    def get_cc(self):
        return ["cc@example.com"]

    def get_from_email(self):
        return ["from@example.com"]

    def get_reply_to(self):
        return ["reply@example.com"]

    def get_email_headers(self):
        return {"Reply-To": "user@example.com"}


class BaseEmailFormMixinTests(test.TestCase):
    @mock.patch('django.template.loader.render_to_string')
    def test_get_message_returns_rendered_message_template(
            self, render_to_string):
        context = {'message': 'an example message.'}

        class TestForm(forms.BaseEmailFormMixin):
            message_template_name = "my_template.html"

            def get_context(self):
                return context

        form = TestForm()

        message = form.get_message()
        self.assertEqual(render_to_string.return_value, message)
        render_to_string.assert_called_once_with(form.message_template_name,
                                                 context)

    @mock.patch('django.template.loader.render_to_string')
    def test_get_subject_returns_single_line_rendered_subject_template(
            self, render_to_string):
        render_to_string.return_value = 'This is \na \ntemplate.'
        context = {'message': 'an example message.'}

        class TestForm(forms.BaseEmailFormMixin):
            subject_template_name = "my_template.html"

            def get_context(self):
                return context

        form = TestForm()

        subject = form.get_subject()
        self.assertEqual('This is a template.', subject)
        render_to_string.assert_called_once_with(form.subject_template_name,
                                                 context)

    def test_get_context_returns_cleaned_data_with_request_when_form_is_valid(
            self):
        request = test.RequestFactory().post("/")

        class TestForm(forms.BaseEmailFormMixin, forms.forms.Form):
            name = forms.forms.CharField()

        form = TestForm(data={'name': 'test'})
        form.request = request
        self.assertEqual(
            dict(name='test', request=request), form.get_context())

    def test_get_context_returns_value_error_when_form_is_invalid(self):
        class TestForm(forms.BaseEmailFormMixin, forms.forms.Form):
            name = forms.forms.CharField()

        form = TestForm(data={})
        with self.assertRaises(ValueError) as ctx:
            form.get_context()
        self.assertEqual("Cannot generate Context when form is invalid.",
                         str(ctx.exception))

    def test_sends_mail_with_message_dict(self):
        mock_request = test.RequestFactory().get('/')

        form = SampleBasicTestForm(data={"field": "thing"})
        form.send_email(mock_request)

        email = mail.outbox[0]
        self.assertEqual(form.recipient_list, email.to)
        self.assertEqual(form.from_email, email.from_email)
        self.assertEqual(form.get_subject(), email.subject)
        self.assertEqual(form.get_message(), email.body)
        self.assertEqual([], email.cc)
        self.assertEqual([], email.bcc)

    def test_send_mail_sets_request_on_instance(self):
        mock_request = test.RequestFactory().get('/')

        form = SampleBasicTestForm(data={"field": "thing"})
        form.send_email(mock_request)
        self.assertEqual(mock_request, form.request)

    def test_gets_message_dict(self):
        # tests default message dict without overrides
        form = SampleBasicTestForm(data={"field": "thing"})
        form.request = test.RequestFactory().get("/")
        message_dict = form.get_message_dict()

        self.assertEqual({
            "from_email": form.from_email,
            "to": form.recipient_list,
            "body": form.get_message(),
            "subject": form.get_subject(),
            "cc": None,
            "bcc": None,
            "reply_to": None,
        }, message_dict)

    def test_get_message_dict_adds_headers_when_present(self):
        form = SampleCustomizedTestForm(data={"field": "thing"})
        form.request = test.RequestFactory().get("/")
        message_dict = form.get_message_dict()

        self.assertEqual(form.get_email_headers(), message_dict["headers"])

    def test_get_message_dict_adds_cc_when_present(self):
        form = SampleCustomizedTestForm(data={"field": "Thing"})
        form.request = test.RequestFactory().get("/")
        message_dict = form.get_message_dict()

        self.assertEqual(["cc@example.com"], message_dict["cc"])

    def test_get_message_dict_adds_bcc_when_present(self):
        form = SampleCustomizedTestForm(data={"field": "Thing"})
        form.request = test.RequestFactory().get("/")
        message_dict = form.get_message_dict()

        self.assertEqual(["bcc@example.com"], message_dict["bcc"])

    def test_get_message_dict_adds_reply_to_when_present(self):
        form = SampleCustomizedTestForm(data={"field": "Thing"})
        form.request = test.RequestFactory().get("/")
        message_dict = form.get_message_dict()

        self.assertEqual(["reply@example.com"], message_dict["reply_to"])


class ContactFormTests(test.TestCase):
    def test_is_subclass_of_form_and_base_contact_form_mixin(self):
        self.assertTrue(
            issubclass(forms.ContactForm, forms.BaseEmailFormMixin))
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
        self.assertTrue(template_exists,
                        "Email message template does not exist")

    def test_sends_mail_with_headers(self):
        class ReplyToForm(forms.ContactForm):
            email = forms.forms.EmailField()

            def get_reply_to(self):
                return [self.cleaned_data['email']]

        mock_request = test.RequestFactory().get('/')
        reply_to_email = u'user@example.com'  # the user's email

        form = ReplyToForm(data={'email': reply_to_email})
        form.send_email(mock_request)

        self.assertEqual(reply_to_email, mail.outbox[0].message()["Reply-To"])


class ContactModelFormTests(test.TestCase):
    def test_is_subclass_of_model_form_and_base_contact_form_mixin(self):
        self.assertTrue(
            issubclass(forms.ContactModelForm, forms.BaseEmailFormMixin))
        self.assertTrue(
            issubclass(forms.ContactModelForm, forms.forms.ModelForm))

    def test_has_valid_subject_template(self):
        template_exists = 1
        try:
            loader.render_to_string(
                forms.ContactModelForm.subject_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists, "Subject template does not exist")

    def test_has_valid_message_template(self):
        template_exists = 1
        try:
            loader.render_to_string(
                forms.ContactModelForm.message_template_name)
        except TemplateDoesNotExist:
            template_exists = 0
        self.assertTrue(template_exists,
                        "Email message template does not exist")
