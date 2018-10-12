from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

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
        'size': 'Medium',
        'content': 'some test content',
    }

    npc_form_data = {
        'name': 'test npc name',
        'level': 1,
        'alignment': 'N',
        'size': 'Medium',
        'content': 'cat goes meow'
    }

    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.players = mommy.make(
            models.Player,
            user=self.users[0],
            _fill_optional=True,
            _quantity=2,
        )
        self.players[1].user = self.users[1]
        self.players[1].save()

        self.monsters = mommy.make(
            models.Monster,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.monsters[1].user = self.users[1]
        self.monsters[1].save()

        self.npcs = mommy.make(
            models.NPC,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.npcs[1].user = self.users[1]
        self.npcs[1].save()

    def test_player_exists(self):
        players = models.Player.objects.all()

        self.assertIn(self.players[0], players)
        self.assertIn(self.players[1], players)

    def test_player_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/player/{}/'.format(self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_player_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/player/{}/'.format(self.players[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_player_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/player/create/')
        self.assertEqual(response.status_code, 200)

    def test_player_create(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/player/create/', self.player_form_data)
        player = models.Player.objects.get(character_name='test character name')
        self.assertRedirects(response, '/characters/player/{}/'.format(player.pk), 302, 200)

        players = models.Player.objects.all()
        self.assertIn(player, players)

    def test_player_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/player/{}/edit/'.format(self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_player_edit(self):
        self.client.force_login(self.users[0])
        self.player_form_data['character_name'] = "test character name EDIT"
        response = self.client.post('/characters/player/{}/edit/'.format(self.players[0].pk), self.player_form_data)
        self.assertRedirects(response, '/characters/player/{}/'.format(self.players[0].pk), 302, 200)

        response = self.client.get('/characters/player/{}/'.format(self.players[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test character name EDIT')

    def test_player_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/player/{}/delete/'.format(self.players[0].pk), {})
        self.assertRedirects(response, '/characters/player/', 302, 200)

        players = models.Player.objects.all()
        self.assertEqual(players.count(), 1)

    def test_monster_exists(self):
        monsters = models.Monster.objects.all()
        self.assertIn(self.monsters[0], monsters)
        self.assertIn(self.monsters[1], monsters)

    def test_monster_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/monster/{}/'.format(self.monsters[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monsters[0].name)
        self.assertContains(response, self.monsters[0].content)

    def test_monster_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/monster/{}/'.format(self.monsters[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_monster_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/monster/create/')
        self.assertEqual(response.status_code, 200)

    def test_monster_create(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/monster/create/', self.monster_form_data)
        monster = models.Monster.objects.get(name='test monster name')
        self.assertRedirects(response, '/characters/monster/{}/'.format(monster.pk), 302, 200)

        monsters = models.Monster.objects.all()
        self.assertIn(monster, monsters)

    def test_monster_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/monster/{}/edit/'.format(self.monsters[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monsters[0].name)

    def test_monster_edit(self):
        self.client.force_login(self.users[0])
        self.monster_form_data['name'] = "test monster name EDIT"
        response = self.client.post('/characters/monster/{}/edit/'.format(self.monsters[0].pk), self.monster_form_data)
        self.assertRedirects(response, '/characters/monster/{}/'.format(self.monsters[0].pk), 302, 200)

        response = self.client.get('/characters/monster/{}/'.format(self.monsters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test monster name EDIT')

    def test_monster_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/monster/{}/delete/'.format(self.monsters[0].pk), {})
        self.assertRedirects(response, '/characters/monster/', 302, 200)

        monsters = models.Monster.objects.all()
        self.assertEqual(monsters.count(), 1)

    def test_npc_exists(self):
        npcs = models.NPC.objects.all()
        self.assertIn(self.npcs[0], npcs)
        self.assertIn(self.npcs[1], npcs)

    def test_npc_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/npc/{}/'.format(self.npcs[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npcs[0].name)
        self.assertContains(response, self.npcs[0].content)

    def test_npc_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/npc/{}/'.format(self.npcs[1].pk))
        self.assertEqual(response.status_code, 404)

    def test_npc_create_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/npc/create/')
        self.assertEqual(response.status_code, 200)

    def test_npc_create(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/npc/create/', self.npc_form_data)
        npc = models.NPC.objects.get(name='test npc name')
        self.assertRedirects(response, '/characters/npc/{}/'.format(npc.pk), 302, 200)

        npcs = models.NPC.objects.all()
        self.assertIn(npc, npcs)

    def test_npc_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/npc/{}/edit/'.format(self.npcs[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npcs[0].name)

    def test_npc_edit(self):
        self.client.force_login(self.users[0])
        self.npc_form_data['name'] = "test npc name EDIT"
        response = self.client.post('/characters/npc/{}/edit/'.format(self.npcs[0].pk), self.npc_form_data)
        self.assertRedirects(response, '/characters/npc/{}/'.format(self.npcs[0].pk), 302, 200)

        response = self.client.get('/characters/npc/{}/'.format(self.npcs[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test npc name EDIT')

    def test_npc_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/characters/npc/{}/delete/'.format(self.npcs[0].pk), {})
        self.assertRedirects(response, '/characters/npc/', 302, 200)

        npcs = models.NPC.objects.all()
        self.assertEqual(npcs.count(), 1)