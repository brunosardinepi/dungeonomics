from django.contrib.auth.models import User
from django.test import Client, TestCase

from . import views


class HomeTest(TestCase):
    def setUp(self):
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.test',
            password='testpassword'
        )

    def test_home_logged_out(self):
        response = self.client.get('/')

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
        self.assertNotContains(response, "Streamlined Roleplaying")

    def test_page_200(self):
        pages = [
            '/',
            '/social-auth/',
        ]

        for page in pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200)
