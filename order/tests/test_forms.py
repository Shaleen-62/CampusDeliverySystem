from django.test import TestCase
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from order.forms import LoginRegisterForm

class TestLoginRegisterForm(TestCase):
    def test_login_register_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        form = LoginRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_register_form_missing_data(self):
        form_data = {
            'username': '',
            'password': '',
        }
        form = LoginRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_register_form_password_widget(self):
        form = LoginRegisterForm()
        self.assertIsInstance(form.fields['password'].widget, PasswordInput)
