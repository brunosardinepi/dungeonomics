from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import models
from . import views


class VoteTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.features = mommy.make(
            models.Feature,
            _quantity=2,
            _fill_optional=True,
        )

    def test_feature_exists(self):
        features = models.Feature.objects.all()
        self.assertIn(self.features[0], features)
        self.assertIn(self.features[1], features)

    def test_feature_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.features[0].description)
        self.assertContains(response, self.features[1].description)

    def test_feature_page_bad_user(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.features[0].description)
        self.assertNotContains(response, self.features[1].description)

    def test_feature_vote_add(self):
        self.assertEqual(self.features[0].votes(), 0)
        self.assertEqual(self.features[1].votes(), 0)

        self.client.force_login(self.users[0])
        response = self.client.get('/votes/{}/'.format(self.features[0].pk))

        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(self.features[0].votes(), 1)
        self.assertEqual(self.features[1].votes(), 0)

        response = self.client.get('/')
        self.assertContains(response, '<span class="badge badge-primary badge-pill ml-3">1</span>')

        self.client.logout()

        self.client.force_login(self.users[1])
        response = self.client.get('/votes/{}/'.format(self.features[0].pk))

        self.assertRedirects(response, '/', 302, 200)
        self.assertEqual(self.features[0].votes(), 2)
        self.assertEqual(self.features[1].votes(), 0)

        response = self.client.get('/')
        self.assertContains(response, '<span class="badge badge-primary badge-pill ml-3">2</span>')

