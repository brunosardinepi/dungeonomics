from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import models
from . import views


class WikiTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.tags = mommy.make(
            models.Tag,
            _quantity=3,
            _fill_optional=True,
        )

        self.articles = mommy.make(
            models.Article,
            _quantity=5,
            _fill_optional=True,
        )

    def test_article_exists(self):
        articles = models.Article.objects.all()
        self.assertIn(self.articles[0], articles)
        self.assertIn(self.articles[1], articles)
        self.assertIn(self.articles[2], articles)
        self.assertIn(self.articles[3], articles)
        self.assertIn(self.articles[4], articles)

    def test_article_page(self):
        response = self.client.get('/wiki/')
        self.assertRedirects(response, '/accounts/login/?next=/wiki/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/wiki/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.articles[0].title)
        self.assertContains(response, self.articles[1].title)
        self.assertContains(response, self.articles[2].title)
        self.assertContains(response, self.articles[3].title)
        self.assertContains(response, self.articles[4].title)

    def test_article_update(self):
        response = self.client.get('/wiki/{}/'.format(self.articles[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/wiki/{}/'.format(self.articles[0].pk),
            302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/wiki/{}/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 200)

        title = "new title"
        description = "new description"
        data = {
            'title': title,
            'description': description,
        }
        response = self.client.post('/wiki/{}/edit/'.format(self.articles[0].pk), data)
        self.assertRedirects(response, '/wiki/{}/'.format(self.articles[0].pk), 302, 200)

        response = self.client.get('/wiki/{}/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertContains(response, description)
        self.assertNotContains(response, self.articles[0].title)
        self.assertNotContains(response, self.articles[0].description)
