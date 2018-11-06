from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from . import forms
from . import models


class CharacterTest(TestCase):
    character_form_data = {
        'name': 'test character name',
        'attribute_set-TOTAL_FORMS': '1',
        'attribute_set-INITIAL_FORMS': '0',
        'attribute_set-MIN_NUM_FORMS': '0',
        'attribute_set-MAX_NUM_FORMS': '1000',
        'attribute_set-0-id': '',
        'attribute_set-0-content': 'o1',
    }

    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.characters = mommy.make(
            models.GeneralCharacter,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.characters[1].user = self.users[1]
        self.characters[1].save()

    def test_character_exists(self):
        characters = models.GeneralCharacter.objects.all()

        self.assertIn(self.characters[0], characters)
        self.assertIn(self.characters[1], characters)

    def test_character_page(self):
        # unauthenticated user
        response = self.client.get('/characters/character/{}/'.format(self.characters[0].pk))
        self.assertRedirects(response,
            '/accounts/login/?next=/characters/character/{}/'.format(self.characters[0].pk),
            302, 200)

        # authenticated user on incorrect character
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/character/{}/'.format(self.characters[1].pk))
        self.assertEqual(response.status_code, 404)

        # authenticated user on correct character
        response = self.client.get('/characters/character/{}/'.format(self.characters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.characters[0].name)
        self.assertContains(response, self.characters[0].name)

    def test_character_create_page(self):
        # unauthenticated user
        response = self.client.get('/characters/character/{}/'.format(self.characters[0].pk))
        self.assertRedirects(response,
            '/accounts/login/?next=/characters/character/{}/'.format(self.characters[0].pk),
            302, 200)

        # authenticated user
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/character/create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/characters/character/create/', self.character_form_data)
        character = models.GeneralCharacter.objects.get(name='test character name')
        self.assertRedirects(response, '/characters/character/{}/'.format(character.pk), 302, 200)

        characters = models.GeneralCharacter.objects.all()
        self.assertIn(character, characters)
