from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from . import forms
from . import models
from . import views


class ItemTest(TestCase):
    item_form_data = {
        'name': 'test item name',
    }

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

        self.item = models.Item.objects.create(
            user=self.user,
            name="test item",
            description="this is test item",
        )

        self.item2 = models.Item.objects.create(
            user=self.user2,
            name="test 2 item",
            description="this is test 2 item",
        )

    def test_item_exists(self):
        items = models.Item.objects.all()
        self.assertIn(self.item, items)
        self.assertIn(self.item2, items)

    def test_item_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/items/{}/'.format(self.item.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertContains(response, self.item.description)

    def test_item_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/items/{}/'.format(self.item2.pk))
        self.assertEqual(response.status_code, 404)

    def test_item_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/items/create/')
        self.assertEqual(response.status_code, 200)

    def test_item_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/items/create/', self.item_form_data)
        item = models.Item.objects.get(name='test item name')
        self.assertRedirects(response, '/items/{}/'.format(item.pk), 302, 200)

        items = models.Item.objects.all()
        self.assertIn(item, items)

    def test_item_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/items/{}/edit/'.format(self.item.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_item_edit(self):
        self.client.login(username='testuser', password='testpassword')
        self.item_form_data['name'] = "test item name EDIT"
        response = self.client.post('/items/{}/edit/'.format(self.item.pk), self.item_form_data)
        self.assertRedirects(response, '/items/{}/'.format(self.item.pk), 302, 200)

        response = self.client.get('/items/{}/'.format(self.item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test item name EDIT')

    def test_item_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/items/{}/delete/'.format(self.item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_item_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/items/{}/delete/'.format(self.item.pk), {})
        self.assertRedirects(response, '/items/', 302, 200)

        items = models.Item.objects.all()
        self.assertEqual(items.count(), 1)