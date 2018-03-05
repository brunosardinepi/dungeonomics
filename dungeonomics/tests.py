import django

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core import mail
from django.db import models
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.timezone import now

from allauth.account.auth_backends import AuthenticationBackend
from allauth.account.forms import BaseSignupForm
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account import app_settings
from allauth.utils import get_user_model, get_username_max_length

from . import views


class HomeTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.test',
            password='testpassword'
        )

    def test_home_logged_out(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Streamlined Roleplaying")
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign up")
        self.assertContains(response, "Features")
        self.assertContains(response, "Users")
        self.assertContains(response, "Campaigns")
        self.assertContains(response, "Creatures")
        self.assertContains(response, "Donate")

    def test_home_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Streamlined Roleplaying")


class AccountTests(TestCase):
    def _create_user(self, username='john', password='doe'):
        user = get_user_model().objects.create(
            username=username,
            is_active=True)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def _create_user_and_login(self, usable_password=True):
        password = 'doe' if usable_password else False
        user = self._create_user(password=password)
        c = self.client
        c.force_login(user)
        return user

    def test_redirect_when_authenticated(self):
        self._create_user_and_login()
        c = self.client
        resp = c.get(reverse('account_login'))
        self.assertRedirects(resp, 'http://localhost/',
                             fetch_redirect_response=False)

    def test_password_reset_get(self):
        resp = self.client.get(reverse('account_reset_password'))
        self.assertTemplateUsed(resp, 'password_reset.html')

    def _password_set_or_change_redirect(self, urlname, usable_password):
        self._create_user_and_login(usable_password)
        return self.client.get(reverse(urlname))

    def test_password_set_redirect(self):
        resp = self._password_set_or_change_redirect(
            'account_set_password',
            True)
        self.assertRedirects(
            resp,
            reverse('account_change_password'),
            fetch_redirect_response=False)

    def test_password_change_no_redirect(self):
        resp = self._password_set_or_change_redirect(
            'account_change_password',
            True)
        self.assertEqual(resp.status_code, 200)

    def test_password_set_no_redirect(self):
        resp = self._password_set_or_change_redirect(
            'account_set_password',
            False)
        self.assertEqual(resp.status_code, 200)

    def test_password_change_redirect(self):
        resp = self._password_set_or_change_redirect(
            'account_change_password',
            False)
        self.assertRedirects(
            resp,
            reverse('account_set_password'),
            fetch_redirect_response=False)

    def _request_new_password(self):
        user = get_user_model().objects.create(
            username='john', email='john@doe.org', is_active=True)
        user.set_password('doe')
        user.save()
        self.client.post(
            reverse('account_reset_password'),
            data={'email': 'john@doe.org'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['john@doe.org'])
        return user

    def _logout_view(self, method):
        c = Client()
        user = get_user_model().objects.create(username='john', is_active=True)
        user.set_password('doe')
        user.save()
        c = Client()
        c.login(username='john', password='doe')
        return c, getattr(c, method)(reverse('account_logout'))

    @override_settings(ACCOUNT_LOGOUT_ON_GET=True)
    def test_logout_view_on_get(self):
        c, resp = self._logout_view('get')
        self.assertTemplateUsed(resp, 'account/messages/logged_out.txt')

    @override_settings(ACCOUNT_LOGOUT_ON_GET=False)
    def test_logout_view_on_post(self):
        c, resp = self._logout_view('get')
        self.assertTemplateUsed(
            resp,
            'account/logout.%s' % app_settings.TEMPLATE_EXTENSION)
        resp = c.post(reverse('account_logout'))
        self.assertTemplateUsed(resp, 'account/messages/logged_out.txt')

    @override_settings(ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS=False)
    def test_account_authenticated_login_redirects_is_false(self):
        self._create_user_and_login()
        resp = self.client.get(reverse('account_login'))
        self.assertEqual(resp.status_code, 200)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[{
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
            }
        }])
    def test_django_password_validation(self):
        if django.VERSION < (1, 9, ):
            return
        resp = self.client.post(
            reverse('account_signup'),
            {'username': 'johndoe',
             'email': 'john@doe.com',
             'password1': 'johndoe',
             'password2': 'johndoe'})
        self.assertFormError(resp, 'form', None, [])
        self.assertFormError(
            resp,
            'form',
            'password1',
            ['This password is too short.'
             ' It must contain at least 9 characters.'])

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=True)
    def test_email_confirmation_hmac_falls_back(self):
        user = self._create_user()
        email = EmailAddress.objects.create(
            user=user,
            email='a@b.com',
            verified=False,
            primary=True)
        confirmation = EmailConfirmation.create(email)
        confirmation.sent = now()
        confirmation.save()
        self.client.post(
            reverse('account_confirm_email',
                    args=[confirmation.key]))
        email = EmailAddress.objects.get(pk=email.pk)
        self.assertTrue(email.verified)

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=True)
    def test_email_confirmation_hmac(self):
        user = self._create_user()
        email = EmailAddress.objects.create(
            user=user,
            email='a@b.com',
            verified=False,
            primary=True)
        confirmation = EmailConfirmationHMAC(email)
        confirmation.send()
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(
            reverse('account_confirm_email',
                    args=[confirmation.key]))
        email = EmailAddress.objects.get(pk=email.pk)
        self.assertTrue(email.verified)

    @override_settings(
        ACCOUNT_EMAIL_CONFIRMATION_HMAC=True,
        ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=0)
    def test_email_confirmation_hmac_timeout(self):
        user = self._create_user()
        email = EmailAddress.objects.create(
            user=user,
            email='a@b.com',
            verified=False,
            primary=True)
        confirmation = EmailConfirmationHMAC(email)
        confirmation.send()
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(
            reverse('account_confirm_email',
                    args=[confirmation.key]))
        email = EmailAddress.objects.get(pk=email.pk)
        self.assertFalse(email.verified)


class EmailFormTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='john',
                                        email='john1@doe.org')
        self.user.set_password('doe')
        self.user.save()
        self.email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True)
        self.email_address2 = EmailAddress.objects.create(
            user=self.user,
            email='john2@doe.org',
            verified=False,
            primary=False)
        self.client.login(username='john', password='doe')

    def test_add(self):
        resp = self.client.post(
            reverse('account_email'),
            {'action_add': '',
             'email': 'john3@doe.org'})
        EmailAddress.objects.get(
            email='john3@doe.org',
            user=self.user,
            verified=False,
            primary=False)
        self.assertTemplateUsed(resp,
                                'account/messages/email_confirmation_sent.txt')

    def test_remove_primary(self):
        resp = self.client.post(
            reverse('account_email'),
            {'action_remove': '',
             'email': self.email_address.email})
        EmailAddress.objects.get(pk=self.email_address.pk)
        self.assertTemplateUsed(
            resp,
            'account/messages/cannot_delete_primary_email.txt')

    def test_remove_secondary(self):
        resp = self.client.post(
            reverse('account_email'),
            {'action_remove': '',
             'email': self.email_address2.email})
        self.assertRaises(EmailAddress.DoesNotExist,
                          lambda: EmailAddress.objects.get(
                              pk=self.email_address2.pk))
        self.assertTemplateUsed(
            resp,
            'account/messages/email_deleted.txt')

    def test_set_primary_unverified(self):
        resp = self.client.post(
            reverse('account_email'),
            {'action_primary': '',
             'email': self.email_address2.email})
        email_address = EmailAddress.objects.get(pk=self.email_address.pk)
        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        self.assertFalse(email_address2.primary)
        self.assertTrue(email_address.primary)
        self.assertTemplateUsed(
            resp,
            'account/messages/unverified_primary_email.txt')

    def test_set_primary(self):
        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        email_address2.verified = True
        email_address2.save()
        resp = self.client.post(
            reverse('account_email'),
            {'action_primary': '',
             'email': self.email_address2.email})
        email_address = EmailAddress.objects.get(pk=self.email_address.pk)
        email_address2 = EmailAddress.objects.get(pk=self.email_address2.pk)
        self.assertFalse(email_address.primary)
        self.assertTrue(email_address2.primary)
        self.assertTemplateUsed(
            resp,
            'account/messages/primary_email_set.txt')

    def test_verify(self):
        resp = self.client.post(
            reverse('account_email'),
            {'action_send': '',
             'email': self.email_address2.email})
        self.assertTemplateUsed(
            resp,
            'account/messages/email_confirmation_sent.txt')


class BaseSignupFormTests(TestCase):

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_USERNAME_BLACKLIST=['username'])
    def test_username_in_blacklist(self):
        data = {
            'username': 'username',
            'email': 'user@example.com',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_USERNAME_BLACKLIST=['username'])
    def test_username_not_in_blacklist(self):
        data = {
            'username': 'theusername',
            'email': 'user@example.com',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertTrue(form.is_valid())

    @override_settings(ACCOUNT_USERNAME_REQUIRED=True)
    def test_username_maxlength(self):
        data = {
            'username': 'username',
            'email': 'user@example.com',
        }
        form = BaseSignupForm(data, email_required=True)
        max_length = get_username_max_length()
        field = form.fields['username']
        self.assertEqual(field.max_length, max_length)
        widget = field.widget
        self.assertEqual(widget.attrs.get('maxlength'), str(max_length))

    @override_settings(
        ACCOUNT_USERNAME_REQUIRED=True,
        ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE=True)
    def test_signup_email_verification(self):
        data = {
            'username': 'username',
            'email': 'user@example.com',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())

        data = {
            'username': 'username',
            'email': 'user@example.com',
            'email2': 'user@example.com',
        }
        form = BaseSignupForm(data, email_required=True)
        self.assertTrue(form.is_valid())

        data['email2'] = 'anotheruser@example.com'
        form = BaseSignupForm(data, email_required=True)
        self.assertFalse(form.is_valid())


class AuthenticationBackendTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(
            is_active=True,
            email='john@doe.com',
            username='john')
        user.set_password(user.username)
        user.save()
        self.user = user

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME)  # noqa
    def test_auth_by_username(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username),
            None)

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.EMAIL)  # noqa
    def test_auth_by_email(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username),
            None)

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=app_settings.AuthenticationMethod.USERNAME_EMAIL)  # noqa
    def test_auth_by_username_or_email(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                username=user.email,
                password=user.username).pk,
            user.pk)
        self.assertEqual(
            backend.authenticate(
                username=user.username,
                password=user.username).pk,
            user.pk)
