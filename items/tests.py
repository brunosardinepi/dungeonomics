from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

import unittest

from . import forms
from . import models
from . import views


class ItemTest(TestCase):
    item_form_data = {
        'name': 'test item',
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test item for testuser
        self.item = models.Item.objects.create(
            user=self.user,
            name="test item",
            description="this is test item",
        )

        # create a test item for testuser2
        self.item2 = models.Item.objects.create(
            user=self.user2,
            name="test 2 item",
            description="this is test 2 item",
        )

    def test_item_exists(self):
        """
        Test items exist
        """

        # get queryset that contains all items
        items = models.Item.objects.all()

        # make sure the test items exist in the queryset
        self.assertIn(self.item, items)
        self.assertIn(self.item2, items)

    def test_item_page(self):
        """
        Item page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.item_detail(request, self.item.pk)

        # make sure the item information is on the page
        self.assertContains(response, self.item.name, status_code=200)
        self.assertContains(response, self.item.description, status_code=200)

    @unittest.expectedFailure
    def test_item_page_bad_user(self):
        """
        Item page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.item_detail(request, self.item2.pk)

    def test_item_create_page(self):
        """
        Create item page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.item_create(request)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_item_create(self):
        """
        Create item
        """

        form = forms.ItemForm(data=self.item_form_data)
        new_item = form.save(commit=False)
        new_item.user = self.user
        new_item.save()

        new_item = models.Item.objects.get(pk=new_item.pk)
        items = models.Item.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_item, items)

    def test_item_edit_page(self):
        """
        Edit item page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.item_update(request, self.item.pk)

        # make sure the item information is on the page
        self.assertContains(response, self.item.name, status_code=200)
        self.assertContains(response, self.item.description, status_code=200)

    def test_item_edit(self):
        """
        Edit item
        """

        self.item_form_data['name'] = "test EDIT item"
        form = forms.ItemForm(data=self.item_form_data)
        new_item = form.save(commit=False)
        new_item.user = self.user
        new_item.save()

        verify_item = models.Item.objects.get(pk=new_item.pk)
        items = models.Item.objects.all()

        self.assertTrue(form.is_valid())
        self.assertEqual(new_item.name, verify_item.name)

    def test_item_delete_page(self):
        """
        Delete item page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.item_delete(request, self.item.pk)

        # make sure the item information is on the page
        self.assertContains(response, self.item.name, status_code=200)

    def test_item_delete(self):
        """
        Delete item
        """

        form = forms.DeleteItemForm(data=self.item_form_data)
        new_item = form.save(commit=False)
        new_item.user = self.user
        new_item.save()

        self.assertTrue(form.is_valid())
