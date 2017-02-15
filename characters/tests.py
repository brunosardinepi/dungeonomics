from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase

import unittest

from . import forms
from . import models
from . import views


class PlayerTest(TestCase):
    player_form_data = {
        'player_name': 'test player name',
        'character_name': 'test character name',
        'alignment': 'N',
        'size': 'Medium',
        'level': 1,
        'name': 'test player name'
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test player for testuser
        self.player = models.Player.objects.create(
            user=self.user,
            player_name="test player",
            character_name="test character",
        )

        # create a test player for testuser2
        self.player2 = models.Player.objects.create(
            user=self.user2,
            player_name="test 2 player",
            character_name="test 2 character",
        )

    def test_player_exists(self):
        """
        Test players exist
        """

        # get queryset that contains all players
        players = models.Player.objects.all()

        # make sure the test players exist in the queryset
        self.assertIn(self.player, players)
        self.assertIn(self.player2, players)

    def test_player_page(self):
        """
        Player page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_detail(request, self.player.pk)

        # make sure the player information is on the page
        self.assertContains(response, self.player.name, status_code=200)
        self.assertContains(response, self.player.character_name, status_code=200)

    @unittest.expectedFailure
    def test_player_page_bad_user(self):
        """
        Player page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_detail(request, self.player2.pk)

    def test_player_create(self):
        """
        Create player
        """

        form = forms.PlayerForm(data=self.player_form_data)
        new_player = form.save(commit=False)
        new_player.user = self.user
        new_player.save()

        new_player = models.Player.objects.get(pk=new_player.pk)
        players = models.Player.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_player, players)

    def test_player_edit_page(self):
        """
        Edit player page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_update(request, self.player.pk)

        # make sure the player information is on the page
        self.assertContains(response, self.player.name, status_code=200)
        self.assertContains(response, self.player.character_name, status_code=200)

    def test_player_edit(self):
        """
        Edit player
        """

        self.player_form_data['name'] = "test player name EDIT"
        form = forms.PlayerForm(data=self.player_form_data)
        new_player = form.save(commit=False)
        new_player.user = self.user
        new_player.save()

        verify_player = models.Player.objects.get(pk=new_player.pk)
        players = models.Player.objects.all()

        self.assertTrue(form.is_valid())
        #self.assertIn(new_player, players)
        self.assertEqual(new_player.name, verify_player.name)

    def test_player_delete_page(self):
        """
        Delete player page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_delete(request, self.player.pk)

        # make sure the player information is on the page
        self.assertContains(response, self.player.name, status_code=200)
        self.assertContains(response, self.player.character_name, status_code=200)

    def test_player_delete(self):
        """
        Delete player
        """

        form = forms.DeletePlayerForm(data=self.player_form_data)
        new_player = form.save(commit=False)
        new_player.user = self.user
        new_player.save()

        self.assertTrue(form.is_valid())


class MonsterTest(TestCase):
    monster_form_data = {
        'name': 'test monster name',
        'level': 1,
        'alignment': 'N',
        'size': 'Medium'
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test monster for testuser
        self.monster = models.Monster.objects.create(
            user=self.user,
            name="test monster",
        )

        # create a test monster for testuser2
        self.monster2 = models.Monster.objects.create(
            user=self.user2,
            name="test 2 monster",
        )

    def test_monster_exists(self):
        """
        Test monsters exist
        """

        # get queryset that contains all monsters
        monsters = models.Monster.objects.all()

        # make sure the test monsters exist in the queryset
        self.assertIn(self.monster, monsters)
        self.assertIn(self.monster2, monsters)

    def test_monster_page(self):
        """
        Monster page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.monster_detail(request, self.monster.pk)

        # make sure the monster information is on the page
        self.assertContains(response, self.monster.name, status_code=200)

    @unittest.expectedFailure
    def test_monster_page_bad_user(self):
        """
        Monster page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_detail(request, self.monster2.pk)

    def test_monster_create(self):
        """
        Create monster
        """

        form = forms.MonsterForm(data=self.monster_form_data)
        new_monster = form.save(commit=False)
        new_monster.user = self.user
        new_monster.save()

        new_monster = models.Monster.objects.get(pk=new_monster.pk)
        monsters = models.Monster.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_monster, monsters)

    def test_monster_edit_page(self):
        """
        Edit monster page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.monster_update(request, self.monster.pk)

        # make sure the monster information is on the page
        self.assertContains(response, self.monster.name, status_code=200)

    def test_monster_edit(self):
        """
        Edit monster
        """

        self.monster_form_data['name'] = "test monster name EDIT"
        form = forms.MonsterForm(data=self.monster_form_data)
        new_monster = form.save(commit=False)
        new_monster.user = self.user
        new_monster.save()

        verify_monster = models.Monster.objects.get(pk=new_monster.pk)
        monsters = models.Monster.objects.all()

        self.assertTrue(form.is_valid())
        #self.assertIn(new_monster, monsters)
        self.assertEqual(new_monster.name, verify_monster.name)

    def test_monster_delete_page(self):
        """
        Delete monster page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.monster_delete(request, self.monster.pk)

        # make sure the monster information is on the page
        self.assertContains(response, self.monster.name, status_code=200)

    def test_monster_delete(self):
        """
        Delete monster
        """

        form = forms.DeleteMonsterForm(data=self.monster_form_data)
        new_monster = form.save(commit=False)
        new_monster.user = self.user
        new_monster.save()

        self.assertTrue(form.is_valid())


class NPCTest(TestCase):
    npc_form_data = {
        'name': 'test npc name',
        'level': 1,
        'alignment': 'N',
        'size': 'Medium',
    }

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test npc for testuser
        self.npc = models.NPC.objects.create(
            user=self.user,
            name="test npc",
        )

        # create a test npc for testuser2
        self.npc2 = models.NPC.objects.create(
            user=self.user2,
            name="test 2 npc",
        )

    def test_npc_exists(self):
        """
        Test npcs exist
        """

        # get queryset that contains all npcs
        npcs = models.NPC.objects.all()

        # make sure the test npcs exist in the queryset
        self.assertIn(self.npc, npcs)
        self.assertIn(self.npc2, npcs)

    def test_npc_page(self):
        """
        NPC page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.npc_detail(request, self.npc.pk)

        # make sure the npc information is on the page
        self.assertContains(response, self.npc.name, status_code=200)

    @unittest.expectedFailure
    def test_npc_page_bad_user(self):
        """
        NPC page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.player_detail(request, self.npc2.pk)

    def test_npc_create(self):
        """
        Create npc
        """

        form = forms.NPCForm(data=self.npc_form_data)
        new_npc = form.save(commit=False)
        new_npc.user = self.user
        new_npc.save()

        new_npc = models.NPC.objects.get(pk=new_npc.pk)
        npcs = models.NPC.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_npc, npcs)

    def test_npc_edit_page(self):
        """
        Edit npc page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.npc_update(request, self.npc.pk)

        # make sure the npc information is on the page
        self.assertContains(response, self.npc.name, status_code=200)

    def test_npc_edit(self):
        """
        Edit npc
        """

        self.npc_form_data['name'] = "test npc name EDIT"
        form = forms.NPCForm(data=self.npc_form_data)
        new_npc = form.save(commit=False)
        new_npc.user = self.user
        new_npc.save()

        verify_npc = models.NPC.objects.get(pk=new_npc.pk)
        npcs = models.NPC.objects.all()

        self.assertTrue(form.is_valid())
        #self.assertIn(new_npc, npcs)
        self.assertEqual(new_npc.name, verify_npc.name)

    def test_npc_delete_page(self):
        """
        Delete npc page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.npc_delete(request, self.npc.pk)

        # make sure the npc information is on the page
        self.assertContains(response, self.npc.name, status_code=200)

    def test_npc_delete(self):
        """
        Delete npc
        """

        form = forms.DeleteNPCForm(data=self.npc_form_data)
        new_npc = form.save(commit=False)
        new_npc.user = self.user
        new_npc.save()

        self.assertTrue(form.is_valid())
