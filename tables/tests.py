from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import forms
from . import models
from . import views


class TableTest(TestCase):
    table_form_data = {
        'name': 'test table name',
        'content': 'yyyyyyuyuyuyyuyu',
        'tableoption_set-TOTAL_FORMS': '1',
        'tableoption_set-INITIAL_FORMS': '0',
        'tableoption_set-MIN_NUM_FORMS': '0',
        'tableoption_set-MAX_NUM_FORMS': '1000',
        'tableoption_set-0-id': '',
        'tableoption_set-0-content': 'o1',
    }


    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.tables = mommy.make(
            models.Table,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.tables[1].user = self.users[1]
        self.tables[1].save()

    def test_table_exists(self):
        tables = models.Table.objects.all()
        self.assertIn(self.tables[0], tables)
        self.assertIn(self.tables[1], tables)

    def test_table_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/tables/{}/'.format(self.tables[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tables[0].name)
        self.assertContains(response, self.tables[0].content)

    def test_table_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/tables/{}/'.format(self.tables[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_table_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/tables/create/')
        self.assertEqual(response.status_code, 200)

    def test_table_create(self):
        self.client.force_login(self.users[0])
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
        self.client.force_login(self.users[0])
        response = self.client.get('/tables/{}/edit/'.format(self.tables[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tables[0].name)

    def test_table_edit(self):
        self.client.force_login(self.users[0])
        self.table_form_data['name'] = "test table name EDIT"
        response = self.client.post('/tables/{}/edit/'.format(self.tables[0].pk), self.table_form_data)
        self.assertRedirects(response, '/tables/{}/'.format(self.tables[0].pk), 302, 200)

        response = self.client.get('/tables/{}/'.format(self.tables[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test table name EDIT')

    def test_table_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/tables/{}/delete/'.format(self.tables[0].pk), {})
        self.assertRedirects(response, '/tables/', 302, 200)

        tables = models.Table.objects.all()
        self.assertEqual(tables.count(), 1)