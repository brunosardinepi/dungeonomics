from django.contrib.auth.models import User
from django.test import Client, TestCase

from model_mommy import mommy

from . import views


class DungeonomicsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

    def test_home_logged_out(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Streamlined Roleplaying")
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign up")
        self.assertContains(response, "Features")
        self.assertContains(response, "Users")
        self.assertContains(response, "Campaigns")
        self.assertContains(response, "Characters")
        self.assertContains(response, "Donate")

    def test_home_logged_in(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Streamlined Roleplaying")

    def test_multiple_delete(self):
        self.client.force_login(self.users[0])

        types = [
            'characters',
            'items',
            'tables',
            'worlds',
        ]

        for type in types:
            response = self.client.get('/{}/delete/'.format(type))
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/{}/delete/'.format(type), {})
            if type == 'worlds':
                self.assertRedirects(response, '/locations/', 302, 200)
            else:
                self.assertRedirects(response, '/{}/'.format(type), 302, 200)
