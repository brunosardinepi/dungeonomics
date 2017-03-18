from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

import unittest

from . import forms
from . import models
from . import views


class SpellTest(TestCase):
    spell_form_data = {
        'name': 'test spell',
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test spell for testuser
        self.spell = models.Spell.objects.create(
            user=self.user,
            name="test spell",
            description="this is test spell",
        )

        # create a test spell for testuser2
        self.spell2 = models.Spell.objects.create(
            user=self.user2,
            name="test 2 spell",
            description="this is test 2 spell",
        )

    def test_spell_exists(self):
        """
        Test spells exist
        """

        # get queryset that contains all spells
        spells = models.Spell.objects.all()

        # make sure the test spells exist in the queryset
        self.assertIn(self.spell, spells)
        self.assertIn(self.spell2, spells)

    def test_spell_page(self):
        """
        spell page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.spell_detail(request, self.spell.pk)

        # make sure the spell information is on the page
        self.assertContains(response, self.spell.name, status_code=200)
        self.assertContains(response, self.spell.description, status_code=200)

    @unittest.expectedFailure
    def test_spell_page_bad_user(self):
        """
        spell page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.spell_detail(request, self.spell2.pk)

    def test_spell_create_page(self):
        """
        Create spell page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.spell_create(request)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_spell_create(self):
        """
        Create spell
        """

        form = forms.SpellForm(data=self.spell_form_data)
        new_spell = form.save(commit=False)
        new_spell.user = self.user
        new_spell.save()

        new_spell = models.Spell.objects.get(pk=new_spell.pk)
        spells = models.Spell.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_spell, spells)

    def test_spell_edit_page(self):
        """
        Edit spell page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.spell_update(request, self.spell.pk)

        # make sure the spell information is on the page
        self.assertContains(response, self.spell.name, status_code=200)
        self.assertContains(response, self.spell.description, status_code=200)

    def test_spell_edit(self):
        """
        Edit spell
        """

        self.spell_form_data['name'] = "test EDIT spell"
        form = forms.SpellForm(data=self.spell_form_data)
        new_spell = form.save(commit=False)
        new_spell.user = self.user
        new_spell.save()

        verify_spell = models.Spell.objects.get(pk=new_spell.pk)
        spells = models.Spell.objects.all()

        self.assertTrue(form.is_valid())
        self.assertEqual(new_spell.name, verify_spell.name)

    def test_spell_delete_page(self):
        """
        Delete spell page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.spell_delete(request, self.spell.pk)

        # make sure the spell information is on the page
        self.assertContains(response, self.spell.name, status_code=200)

    def test_spell_delete(self):
        """
        Delete spell
        """

        form = forms.DeleteSpellForm(data=self.spell_form_data)
        new_spell = form.save(commit=False)
        new_spell.user = self.user
        new_spell.save()

        self.assertTrue(form.is_valid())
