from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from . import forms
from . import models
from . import views


class LocationTest(TestCase):
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

        self.world = models.World.objects.create(
            user=self.user,
            name="test world",
            content="this is test world",
        )

        self.world2 = models.World.objects.create(
            user=self.user2,
            name="test 2 world",
            content="this is test 2 world",
        )

        self.location = models.Location.objects.create(
            user=self.user,
            name="test location",
            world=self.world,
            content="this is test location",
        )

        self.location2 = models.Location.objects.create(
            user=self.user2,
            name="test 2 location",
            world=self.world2,
            content="this is test 2 location",
        )

        self.location3 = models.Location.objects.create(
            user=self.user2,
            name="test 3 location",
            world=self.world2,
            parent_location=self.location2,
            content="this is test 3 location",
        )

        self.world_form_data = {
            'name': 'test world name',
            'content': 'this is test world',
        }

        self.location_form_data = {
            'name': 'test location name',
            'content': 'location test',
            'world': self.world2.pk,
            'parent_location': self.location2.pk,
        }

    def test_world_exists(self):
        worlds = models.World.objects.all()
        self.assertIn(self.world, worlds)
        self.assertIn(self.world2, worlds)

    def test_world_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/world/{}/'.format(self.world.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.world.name)
        self.assertContains(response, self.world.content)

    def test_world_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/world/{}/'.format(self.world2.pk))
        self.assertEqual(response.status_code, 404)

    def test_world_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/world/create/')
        self.assertEqual(response.status_code, 200)

    def test_world_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/locations/world/create/', self.world_form_data)
        world = models.World.objects.get(name='test world name')
        self.assertRedirects(response, '/locations/world/{}/'.format(world.pk), 302, 200)

        worlds = models.World.objects.all()
        self.assertIn(world, worlds)

    def test_world_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/world/{}/edit/'.format(self.world.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.world.name)

    def test_world_edit(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'name': 'test world name EDIT',
            'content': 'this is test world',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.location.pk,
            'form-0-order': 1,
            'form-0-name': self.location.name,
        }

        response = self.client.post('/locations/world/{}/edit/'.format(self.world.pk), data)
        self.assertRedirects(response, '/locations/world/{}/'.format(self.world.pk), 302, 200)

        response = self.client.get('/locations/world/{}/'.format(self.world.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test world name EDIT')

    def test_world_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/locations/world/{}/delete/'.format(self.world.pk), {})
        self.assertRedirects(response, '/locations/', 302, 200)

        worlds = models.World.objects.all()
        self.assertEqual(worlds.count(), 1)

    def test_location_exists(self):
        locations = models.Location.objects.all()
        self.assertIn(self.location, locations)
        self.assertIn(self.location2, locations)

    def test_location_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/location/{}/'.format(self.location.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.name)
        self.assertContains(response, self.location.content)

    def test_location_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/location/{}/'.format(self.location2.pk))
        self.assertEqual(response.status_code, 404)

    def test_location_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/world/{}/location/create/'.format(self.world.pk))
        self.assertEqual(response.status_code, 200)

    def test_location_create(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post('/locations/world/{}/location/create/'.format(self.world2.pk), self.location_form_data)
        location = models.Location.objects.get(name='test location name')
        self.assertRedirects(response, '/locations/location/{}/'.format(location.pk), 302, 200)

        locations = models.Location.objects.all()
        self.assertIn(location, locations)

    def test_location_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/locations/location/{}/edit/'.format(self.location.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.name)

    def test_location_edit(self):
        self.client.login(username='testuser2', password='testpassword')
        self.location_form_data['name'] = "test location name EDIT"
        response = self.client.post('/locations/location/{}/edit/'.format(self.location3.pk), self.location_form_data)
        self.assertRedirects(response, '/locations/location/{}/'.format(self.location3.pk), 302, 200)

        response = self.client.get('/locations/location/{}/'.format(self.location3.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test location name EDIT')

    def test_location_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/locations/location/{}/delete/'.format(self.location.pk), {})
        self.assertRedirects(response, '/locations/', 302, 200)

        locations = models.Location.objects.all()
        self.assertEqual(locations.count(), 2)