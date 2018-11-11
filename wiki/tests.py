from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import models
from . import views
from dungeonomics import config


class WikiTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=3)
        self.users[0].email = config.settings['wiki_admins'][0]
        self.users[0].save()

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
        self.articles[0].admins.add(self.users[0])
        self.articles[0].admins.add(self.users[2])
        self.articles[0].tags.add(self.tags[0])
        self.articles[1].tags.add(self.tags[1])
        self.articles[2].tags.add(self.tags[1])
        self.articles[3].tags.add(self.tags[2])
        self.articles[4].tags.add(self.tags[2])

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

    def test_article_create(self):
        # unauthenticated user
        response = self.client.get('/wiki/create/')
        self.assertRedirects(
            response,
            '/accounts/login/?next=/wiki/create/',
            302, 200)

        # authenticated, but not an admin
        self.client.force_login(self.users[1])
        response = self.client.get('/wiki/create/')
        self.assertEqual(response.status_code, 404)

        # authenticated wiki admin
        self.client.force_login(self.users[0])
        response = self.client.get('/wiki/create/')
        self.assertEqual(response.status_code, 200)

        title = "new title"
        description = "new description"
        data = {
            'title': title,
            'description': description,
            'tags': self.tags[0].pk,
        }
        response = self.client.post('/wiki/create/', data)
        articles = models.Article.objects.all().order_by('-date')
        self.assertRedirects(response, '/wiki/{}/'.format(articles[0].pk), 302, 200)

        response = self.client.get('/wiki/{}/'.format(articles[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertContains(response, description)

    def test_article_update(self):
        # unauthenticated user
        response = self.client.get('/wiki/{}/edit/'.format(self.articles[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/wiki/{}/edit/'.format(self.articles[0].pk),
            302, 200)

        # authenticated, but not an admin
        self.client.force_login(self.users[1])
        response = self.client.get('/wiki/{}/edit/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 404)

        # authenticated article admin
        self.client.force_login(self.users[0])
        response = self.client.get('/wiki/{}/edit/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 200)

        title = "new title"
        description = "new description"
        data = {
            'title': title,
            'description': description,
            'tags': self.tags[1].pk,
        }
        response = self.client.post('/wiki/{}/edit/'.format(self.articles[0].pk), data)
        self.assertRedirects(response, '/wiki/{}/'.format(self.articles[0].pk), 302, 200)

        response = self.client.get('/wiki/{}/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertContains(response, description)
        self.assertNotContains(response, self.articles[0].title)
        self.assertNotContains(response, self.articles[0].description)

    def test_article_delete(self):
        # unauthenticated user
        response = self.client.get('/wiki/{}/delete/'.format(self.articles[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/wiki/{}/delete/'.format(self.articles[0].pk),
            302, 200)

        # authenticated, but not an admin
        self.client.force_login(self.users[1])
        response = self.client.get('/wiki/{}/delete/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 404)

        # authenticated, article admin, but not a wiki admin
        self.client.force_login(self.users[2])
        response = self.client.get('/wiki/{}/delete/'.format(self.articles[0].pk))
        self.assertEqual(response.status_code, 404)

        # authenticated wiki admin
        self.client.force_login(self.users[0])
        response = self.client.get('/wiki/{}/delete/'.format(self.articles[0].pk))
        self.assertRedirects(response, '/wiki/', 302, 200)

        response = self.client.get('/wiki/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.articles[0].title)
