from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import forms
from . import models
from . import views


class LocationTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.worlds = mommy.make(
            models.World,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.worlds[1].user = self.users[1]
        self.worlds[1].save()

        self.locations = mommy.make(
            models.Location,
            user=self.users[0],
            world=self.worlds[0],
            parent_location=None,
            _quantity=3,
            _fill_optional=True,
        )
        self.locations[1].user = self.users[1]
        self.locations[1].world = self.worlds[1]
        self.locations[1].save()
        self.locations[2].user = self.users[1]
        self.locations[2].world = self.worlds[1]
        self.locations[2].parent_location = self.locations[1]
        self.locations[2].save()

        self.world_form_data = {
            'name': 'test world name',
            'content': 'this is test world',
        }

        self.location_form_data = {
            'name': 'test location name',
            'content': 'location test',
            'world': self.worlds[1].pk,
            'parent_location': self.locations[1].pk,
        }

    def test_world_exists(self):
        worlds = models.World.objects.all()
        self.assertIn(self.worlds[0], worlds)
        self.assertIn(self.worlds[1], worlds)

    def test_world_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/world/{}/'.format(self.worlds[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worlds[0].name)
        self.assertContains(response, self.worlds[0].content)

    def test_world_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/world/{}/'.format(self.worlds[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_world_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/world/create/')
        self.assertEqual(response.status_code, 200)

    def test_world_create(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/locations/world/create/', self.world_form_data)
        world = models.World.objects.get(name='test world name')
        self.assertRedirects(response, '/locations/world/{}/'.format(world.pk), 302, 200)

        worlds = models.World.objects.all()
        self.assertIn(world, worlds)

    def test_world_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/world/{}/edit/'.format(self.worlds[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worlds[0].name)

    def test_world_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'name': 'test world name EDIT',
            'content': 'this is test world',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.locations[0].pk,
            'form-0-order': 1,
            'form-0-name': self.locations[0].name,
        }

        response = self.client.post('/locations/world/{}/edit/'.format(self.worlds[0].pk), data)
        self.assertRedirects(response, '/locations/world/{}/'.format(self.worlds[0].pk), 302, 200)

        response = self.client.get('/locations/world/{}/'.format(self.worlds[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test world name EDIT')

    def test_world_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/locations/world/{}/delete/'.format(self.worlds[0].pk), {})
        self.assertRedirects(response, '/locations/', 302, 200)

        worlds = models.World.objects.all()
        self.assertEqual(worlds.count(), 1)

    def test_location_exists(self):
        locations = models.Location.objects.all()
        self.assertIn(self.locations[0], locations)
        self.assertIn(self.locations[1], locations)

    def test_location_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/location/{}/'.format(self.locations[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.locations[0].name)
        self.assertContains(response, self.locations[0].content)

    def test_location_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/location/{}/'.format(self.locations[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_location_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/world/{}/location/create/'.format(self.worlds[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_location_create(self):
        self.client.force_login(self.users[1])
        response = self.client.post('/locations/world/{}/location/create/'.format(self.worlds[1].pk), self.location_form_data)
        location = models.Location.objects.get(name='test location name')
        self.assertRedirects(response, '/locations/location/{}/'.format(location.pk), 302, 200)

        locations = models.Location.objects.all()
        self.assertIn(location, locations)

    def test_location_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/locations/location/{}/edit/'.format(self.locations[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.locations[0].name)

    def test_location_edit(self):
        self.client.force_login(self.users[1])
        self.location_form_data['name'] = "test location name EDIT"
        response = self.client.post('/locations/location/{}/edit/'.format(self.locations[2].pk), self.location_form_data)
        self.assertRedirects(response, '/locations/location/{}/'.format(self.locations[2].pk), 302, 200)

        response = self.client.get('/locations/location/{}/'.format(self.locations[2].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test location name EDIT')

    def test_location_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/locations/location/{}/delete/'.format(self.locations[0].pk), {})
        self.assertRedirects(response, '/locations/', 302, 200)

        locations = models.Location.objects.all()
        self.assertEqual(locations.count(), 2)