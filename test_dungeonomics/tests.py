from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from . import views

class HomeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@email.com', password='password')

    def test_home_view(self):
        request = self.factory.get('home')
        request.user = AnonymousUser()
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # def test_home_view_not_logged_in(self):
    #     request = self.factory.get('home')
    #     request.user = AnonymousUser()
    #     response = views.HomeView.as_view()(request)
    #     self.assertContains(response, '<p>Not logged in</p>')

    # def test_home_view_logged_in(self):
    #     request = self.factory.get('home')
    #     request.user = self.user
    #     response = views.HomeView.as_view()(request)
    #     self.assertContains(response, '<p>Yes logged in</p>')