from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from . import models
from . import views


class VoteTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.test',
            password='testpassword',
        )

        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@test.test',
            password='testpassword',
        )

        self.feature = models.Feature.objects.create(
            description="this is test feature",
        )

        self.feature2 = models.Feature.objects.create(
            description="super feature number two",
        )

    def test_feature_exists(self):
        features = models.Feature.objects.all()
        self.assertIn(self.feature, features)
        self.assertIn(self.feature2, features)

    def test_feature_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feature.description)
        self.assertContains(response, self.feature2.description)

    def test_feature_page_bad_user(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.feature.description)
        self.assertNotContains(response, self.feature2.description)

    def test_feature_vote_add(self):
        self.assertEqual(self.feature.votes(), 0)
        self.assertEqual(self.feature2.votes(), 0)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/votes/{}/'.format(self.feature.pk))

        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(self.feature.votes(), 1)
        self.assertEqual(self.feature2.votes(), 0)

        response = self.client.get('/')
        self.assertContains(response, '<span class="badge badge-primary badge-pill ml-3">1</span>')

        self.client.logout()

        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get('/votes/{}/'.format(self.feature.pk))

        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(self.feature.votes(), 2)
        self.assertEqual(self.feature2.votes(), 0)

        response = self.client.get('/')
        self.assertContains(response, '<span class="badge badge-primary badge-pill ml-3">2</span>')

