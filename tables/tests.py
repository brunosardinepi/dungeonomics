from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from . import forms
from . import models
from . import views


class TableTest(TestCase):
    table_form_data = {
        'name': 'test table name',
        'description': 'yyyyyyuyuyuyyuyu',
#        'order': '2',
        'tableoption_set-TOTAL_FORMS': '1',
        'tableoption_set-INITIAL_FORMS': '0',
        'tableoption_set-MIN_NUM_FORMS': '0',
        'tableoption_set-MAX_NUM_FORMS': '1000',
        'tableoption_set-0-id': '',
        'tableoption_set-0-description': 'o1',
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

        self.table = models.Table.objects.create(
            user=self.user,
            name="test table",
            description="this is test table",
        )

        self.table2 = models.Table.objects.create(
            user=self.user2,
            name="test 2 table",
            description="this is test 2 table",
        )

    def test_table_exists(self):
        tables = models.Table.objects.all()
        self.assertIn(self.table, tables)
        self.assertIn(self.table2, tables)

    def test_table_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tables/{}/'.format(self.table.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.table.name)
        self.assertContains(response, self.table.description)

    def test_table_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tables/{}/'.format(self.table2.pk))
        self.assertEqual(response.status_code, 404)

    def test_table_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tables/create/')
        self.assertEqual(response.status_code, 200)

    def test_table_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/tables/create/', self.table_form_data)
        table = models.Table.objects.get(name='test table name')
        self.assertRedirects(response, '/tables/{}/'.format(table.pk), 302, 200)

        tables = models.Table.objects.all()
        self.assertIn(table, tables)

        response = self.client.get('/tables/{}/'.format(table.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, table.name)
        self.assertContains(response, 'o1')

    def test_table_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tables/{}/edit/'.format(self.table.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.table.name)

    def test_table_edit(self):
        self.client.login(username='testuser', password='testpassword')
        self.table_form_data['name'] = "test table name EDIT"
        response = self.client.post('/tables/{}/edit/'.format(self.table.pk), self.table_form_data)
        self.assertRedirects(response, '/tables/{}/'.format(self.table.pk), 302, 200)

        response = self.client.get('/tables/{}/'.format(self.table.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test table name EDIT')

    def test_table_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/tables/{}/delete/'.format(self.table.pk), {})
        self.assertRedirects(response, '/tables/', 302, 200)

        tables = models.Table.objects.all()
        self.assertEqual(tables.count(), 1)