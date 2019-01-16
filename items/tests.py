from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import forms
from . import models
from . import views


class ItemTest(TestCase):
    item_form_data = {
        'name': 'test item name',
    }

    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.items = mommy.make(
            models.Item,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.items[1].user = self.users[1]
        self.items[1].save()

    def test_item_exists(self):
        items = models.Item.objects.all()
        self.assertIn(self.items[0], items)
        self.assertIn(self.items[1], items)

    def test_item_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/'.format(self.items[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.items[0].name)
        self.assertContains(response, self.items[0].content)

    def test_item_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/'.format(self.items[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_item_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/create/')
        self.assertEqual(response.status_code, 200)

    def test_item_create(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/items/create/', self.item_form_data)
        item = models.Item.objects.get(name='test item name')
        self.assertRedirects(response, '/items/{}/'.format(item.pk), 302, 200)

        items = models.Item.objects.all()
        self.assertIn(item, items)

    def test_item_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/edit/'.format(self.items[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.items[0].name)

    def test_item_edit(self):
        self.client.force_login(self.users[0])
        self.item_form_data['name'] = "test item name EDIT"
        response = self.client.post('/items/{}/edit/'.format(self.items[0].pk), self.item_form_data)
        self.assertRedirects(response, '/items/{}/'.format(self.items[0].pk), 302, 200)

        response = self.client.get('/items/{}/'.format(self.items[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test item name EDIT')

    def test_item_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/items/{}/delete/'.format(self.items[0].pk), {})
        self.assertRedirects(response, '/items/', 302, 200)

        items = models.Item.objects.all()
        self.assertEqual(items.count(), 1)

    def test_item_export(self):
        response = self.client.get('/items/export/')
        self.assertRedirects(response,
            '/accounts/login/?next=/items/export/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/items/export/')
        self.assertEqual(response.status_code, 200)

    def test_item_import(self):
        response = self.client.get('/items/import/')
        self.assertRedirects(response,
            '/accounts/login/?next=/items/import/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/items/import/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/items/import/')
