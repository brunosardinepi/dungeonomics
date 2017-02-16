from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

import unittest

from . import forms
from . import models
from . import views


class LocationTest(TestCase):
    world_form_data = {
        'name': 'test world',
        'content': 'this is test world',
    }

    location_form_data = {
        'name': 'test location',
        'content': 'location test',
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test world for testuser
        self.world = models.World.objects.create(
            user=self.user,
            name="test world",
            content="this is test world",
        )

        # create a test world for testuser2
        self.world2 = models.World.objects.create(
            user=self.user2,
            name="test 2 world",
            content="this is test 2 world",
        )

        # create a test location for testuser
        self.location = models.Location.objects.create(
            user=self.user,
            name="test location",
            world=self.world,
            content="this is test location",
        )

        # create a test location for testuser2
        self.location2 = models.Location.objects.create(
            user=self.user2,
            name="test 2 location",
            world=self.world2,
            content="this is test 2 location",
        )

    def test_world_exists(self):
        """
        Test worlds exist
        """

        # get queryset that contains all worlds
        worlds = models.World.objects.all()

        # make sure the test worlds exist in the queryset
        self.assertIn(self.world, worlds)
        self.assertIn(self.world2, worlds)

    def test_world_page(self):
        """
        Location page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_detail(request, world_pk=self.world.pk)

        # make sure the world information is on the page
        self.assertContains(response, self.world.name, status_code=200)
        self.assertContains(response, self.world.content, status_code=200)

    @unittest.expectedFailure
    def test_world_page_bad_user(self):
        """
        Location page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_detail(request, world_pk=self.world2.pk)

    def test_world_create_page(self):
        """
        Create world page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.world_create(request)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_world_create(self):
        """
        Create world
        """

        form = forms.WorldForm(data=self.world_form_data)
        new_world = form.save(commit=False)
        new_world.user = self.user
        new_world.save()

        new_world = models.World.objects.get(pk=new_world.pk)
        worlds = models.World.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_world, worlds)

    def test_world_edit_page(self):
        """
        Edit world page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.world_update(request, self.world.pk)

        # make sure the world information is on the page
        self.assertContains(response, self.world.name, status_code=200)
        self.assertContains(response, self.world.content, status_code=200)

    def test_world_edit(self):
        """
        Edit world
        """

        self.world_form_data['name'] = "test EDIT world"
        form = forms.WorldForm(data=self.world_form_data)
        new_world = form.save(commit=False)
        new_world.user = self.user
        new_world.save()

        verify_world = models.World.objects.get(pk=new_world.pk)
        worlds = models.World.objects.all()

        self.assertTrue(form.is_valid())
        self.assertEqual(new_world.name, verify_world.name)

    def test_world_delete_page(self):
        """
        Delete world page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.world_delete(request, self.world.pk)

        # make sure the world information is on the page
        self.assertContains(response, self.world.name, status_code=200)

    def test_world_delete(self):
        """
        Delete world
        """

        form = forms.DeleteWorldForm(data=self.world_form_data)
        new_world = form.save(commit=False)
        new_world.user = self.user
        new_world.save()

        self.assertTrue(form.is_valid())

    def test_location_exists(self):
        """
        Test locations exist
        """

        # get queryset that contains all locations
        locations = models.Location.objects.all()

        # make sure the test locations exist in the queryset
        self.assertIn(self.location, locations)
        self.assertIn(self.location2, locations)

    def test_location_page(self):
        """
        Location page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_detail(request, location_pk=self.location.pk)

        # make sure the location information is on the page
        self.assertContains(response, self.location.name, status_code=200)
        self.assertContains(response, self.location.content, status_code=200)

    @unittest.expectedFailure
    def test_location_page_bad_user(self):
        """
        Location page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_detail(request, self.location2.pk)

    def test_location_create_page(self):
        """
        Create location page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_create(request, world_pk=self.world.pk)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_location_create(self):
        """
        Create location
        """

        self.location_form_data['world'] = self.world.pk
        form = forms.LocationForm(self.user.pk, self.world.pk, self.location.pk, data=self.location_form_data)
        new_location = form.save(commit=False)
        new_location.user = self.user
        new_location.save()

        new_location = models.Location.objects.get(pk=new_location.pk)
        locations = models.Location.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_location, locations)

    def test_location_edit_page(self):
        """
        Edit location page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_update(request, self.location.pk)

        # make sure the location information is on the page
        self.assertContains(response, self.location.name, status_code=200)
        self.assertContains(response, self.location.content, status_code=200)

    def test_location_edit(self):
        """
        Edit location
        """

        self.location_form_data['name'] = "test EDIT location"
        self.location_form_data['world'] = self.world.pk
        form = forms.LocationForm(self.user.pk, self.world.pk, self.location.pk, data=self.location_form_data)
        new_location = form.save(commit=False)
        new_location.user = self.user
        new_location.save()

        verify_location = models.Location.objects.get(pk=new_location.pk)
        locations = models.Location.objects.all()

        self.assertTrue(form.is_valid())
        self.assertEqual(new_location.name, verify_location.name)

    def test_location_delete_page(self):
        """
        Delete location page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.location_delete(request, self.location.pk)

        # make sure the location information is on the page
        self.assertContains(response, self.location.name, status_code=200)

    def test_location_delete(self):
        """
        Delete location
        """

        form = forms.DeleteLocationForm(data=self.location_form_data)
        new_location = form.save(commit=False)
        new_location.user = self.user
        new_location.world = self.world
        new_location.save()

        self.assertTrue(form.is_valid())
