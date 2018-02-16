from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from . import forms
from . import models


class CharacterTest(TestCase):
    player_form_data = {
        'player_name': 'test player name',
        'character_name': 'test character name',
        'alignment': 'N',
        'size': 'Medium',
        'level': 1,
        'name': 'test player name'
    }

    monster_form_data = {
        'name': 'test monster name',
        'level': 1,
        'alignment': 'N',
        'size': 'Medium'
    }

    npc_form_data = {
        'name': 'test npc name',
        'level': 1,
        'alignment': 'N',
        'size': 'Medium',
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

        self.player = models.Player.objects.create(
            user=self.user,
            player_name="test player",
            character_name="test character",
        )

        self.player2 = models.Player.objects.create(
            user=self.user2,
            player_name="test 2 player",
            character_name="test 2 character",
        )

        self.monster = models.Monster.objects.create(
            user=self.user,
            name="test monster",
        )

        self.monster2 = models.Monster.objects.create(
            user=self.user2,
            name="test 2 monster",
        )

        self.npc = models.NPC.objects.create(
            user=self.user,
            name="test npc",
        )

        self.npc2 = models.NPC.objects.create(
            user=self.user2,
            name="test 2 npc",
        )

    def test_player_exists(self):
        players = models.Player.objects.all()

        self.assertIn(self.player, players)
        self.assertIn(self.player2, players)

    def test_player_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/player/{}/'.format(self.player.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertContains(response, self.player.character_name)

    def test_player_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/player/{}/'.format(self.player2.pk))
        self.assertEqual(response.status_code, 404)

    def test_player_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/player/create/')
        self.assertEqual(response.status_code, 200)

    def test_player_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/player/create/', self.player_form_data)
        player = models.Player.objects.get(character_name='test character name')
        self.assertRedirects(response, '/characters/player/{}/'.format(player.pk), 302, 200)

        players = models.Player.objects.all()
        self.assertIn(player, players)

    def test_player_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/player/{}/edit/'.format(self.player.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertContains(response, self.player.character_name)

    def test_player_edit(self):
        self.client.login(username='testuser', password='testpassword')
        self.player_form_data['character_name'] = "test character name EDIT"
        response = self.client.post('/characters/player/{}/edit/'.format(self.player.pk), self.player_form_data)
        self.assertRedirects(response, '/characters/player/{}/'.format(self.player.pk), 302, 200)

        response = self.client.get('/characters/player/{}/'.format(self.player.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test character name EDIT')

    def test_player_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/player/{}/delete/'.format(self.player.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.player.name)
        self.assertContains(response, self.player.character_name)

    def test_player_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/player/{}/delete/'.format(self.player.pk), {})
        self.assertRedirects(response, '/characters/player/', 302, 200)

        players = models.Player.objects.all()
        self.assertEqual(players.count(), 1)

    def test_monster_exists(self):
        monsters = models.Monster.objects.all()
        self.assertIn(self.monster, monsters)
        self.assertIn(self.monster2, monsters)

    def test_monster_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/monster/{}/'.format(self.monster.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monster.name)

    def test_monster_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/monster/{}/'.format(self.monster2.pk))
        self.assertEqual(response.status_code, 404)

    def test_monster_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/monster/create/')
        self.assertEqual(response.status_code, 200)

    def test_monster_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/monster/create/', self.monster_form_data)
        monster = models.Monster.objects.get(name='test monster name')
        self.assertRedirects(response, '/characters/monster/{}/'.format(monster.pk), 302, 200)

        monsters = models.Monster.objects.all()
        self.assertIn(monster, monsters)

    def test_monster_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/monster/{}/edit/'.format(self.monster.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monster.name)

    def test_monster_edit(self):
        self.client.login(username='testuser', password='testpassword')
        self.monster_form_data['name'] = "test monster name EDIT"
        response = self.client.post('/characters/monster/{}/edit/'.format(self.monster.pk), self.monster_form_data)
        self.assertRedirects(response, '/characters/monster/{}/'.format(self.monster.pk), 302, 200)

        response = self.client.get('/characters/monster/{}/'.format(self.monster.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test monster name EDIT')

    def test_monster_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/monster/{}/delete/'.format(self.monster.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monster.name)

    def test_monster_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/monster/{}/delete/'.format(self.monster.pk), {})
        self.assertRedirects(response, '/characters/monster/', 302, 200)

        monsters = models.Monster.objects.all()
        self.assertEqual(monsters.count(), 1)

    def test_npc_exists(self):
        npcs = models.NPC.objects.all()
        self.assertIn(self.npc, npcs)
        self.assertIn(self.npc2, npcs)

    def test_npc_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/npc/{}/'.format(self.npc.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npc.name)

    def test_npc_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/npc/{}/'.format(self.npc2.pk))
        self.assertEqual(response.status_code, 404)

    def test_npc_create_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/npc/create/')
        self.assertEqual(response.status_code, 200)

    def test_npc_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/npc/create/', self.npc_form_data)
        npc = models.NPC.objects.get(name='test npc name')
        self.assertRedirects(response, '/characters/npc/{}/'.format(npc.pk), 302, 200)

        npcs = models.NPC.objects.all()
        self.assertIn(npc, npcs)

    def test_npc_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/npc/{}/edit/'.format(self.npc.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npc.name)

    def test_npc_edit(self):
        self.client.login(username='testuser', password='testpassword')
        self.npc_form_data['name'] = "test npc name EDIT"
        response = self.client.post('/characters/npc/{}/edit/'.format(self.npc.pk), self.npc_form_data)
        self.assertRedirects(response, '/characters/npc/{}/'.format(self.npc.pk), 302, 200)

        response = self.client.get('/characters/npc/{}/'.format(self.npc.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test npc name EDIT')

    def test_npc_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/characters/npc/{}/delete/'.format(self.npc.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npc.name)

    def test_npc_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/characters/npc/{}/delete/'.format(self.npc.pk), {})
        self.assertRedirects(response, '/characters/npc/', 302, 200)

        npcs = models.NPC.objects.all()
        self.assertEqual(npcs.count(), 1)