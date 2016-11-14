from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from . import forms


class UserTestCase(TestCase):
    def test_signup_form_success(self):
        """Successfully signup with correct values"""
        form_data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_bad_username_1(self):
        """Fail to signup because of no username"""
        form_data = {
            'username': '',
            'email': 'test@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_bad_username_2(self):
        """Fail to signup because of a username that is over 255 characters"""
        form_data = {
            'username': 'lkjahsdfkljhqwiuehflakjsdhflkjhsadlfiuhqoeiuryqoweiurhlkjsdlakjfnlkjsadhflkjahsdfkljhqwiuehflakjsdhflkjhsadlfiuhqoeiuryqoweiurhlkjsdlakjfnlkjsadhflkjahsdfkljhqwiuehflakjsdhflkjhsadlfiuhqoeiuryqoweiurhlkjsdlakjfnlkjsadhflkjahsdfkljhqwiuehflakjsdhflkjhsadlfiuhqoeiuryqoweiurhlkjsdlakjfnlkjsadhf',
            'email': 'test@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_bad_email_1(self):
        """Fail to signup because of a bad email"""
        form_data = {
            'username': 'testuser',
            'email': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_bad_email_2(self):
        """Fail to signup because of a bad email"""
        form_data = {
            'username': 'testuser',
            'email': 'test@email',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_bad_email_3(self):
        """Fail to signup because of no email"""
        form_data = {
            'username': 'testuser',
            'email': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_password_mismatch(self):
        """Fail to signup because passwords don't match"""
        form_data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password1': 'testpassword',
            'password2': 'badpassword',
            }
        form = forms.UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())