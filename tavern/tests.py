from datetime import timedelta
from random import randint

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from model_mommy import mommy

from campaign.models import Campaign, Chapter, Section
from characters.models import Monster, NPC, Player
from tavern.models import Review


class TavernTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=5)

        self.campaigns = mommy.make(
            Campaign,
            user=self.users[0],
            is_published=True,
            _quantity=2,
            _fill_optional=True,
        )
        self.campaigns[1].user = self.users[1]
        self.campaigns[1].is_published = False
        self.campaigns[1].save()

        self.chapters = mommy.make(
            Chapter,
            user=self.users[0],
            campaign=self.campaigns[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.chapters[1].user = self.users[1]
        self.chapters[1].campaign = self.campaigns[1]
        self.chapters[1].save()

        self.sections = mommy.make(
            Section,
            user=self.users[0],
            chapter=self.chapters[0],
            campaign=self.campaigns[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.sections[1].user = self.users[1]
        self.sections[1].campaign = self.campaigns[1]
        self.sections[1].chapter = self.chapters[1]
        self.sections[1].save()

        self.monsters = mommy.make(
            Monster,
            user=self.users[0],
            is_published=True,
            _quantity=15,
            _fill_optional=True,
        )
        self.monsters[0].published_date = timezone.now()
        self.monsters[0].save()
        self.monsters[1].published_date = timezone.now() + timedelta(days=1)
        self.monsters[1].save()
        self.monsters[2].published_date = timezone.now() + timedelta(days=2)
        self.monsters[2].save()
        self.monsters[3].published_date = timezone.now() + timedelta(days=3)
        self.monsters[3].save()
        self.monsters[4].published_date = timezone.now() + timedelta(days=4)
        self.monsters[4].save()
        self.monsters[5].published_date = timezone.now() + timedelta(days=5)
        self.monsters[5].save()
        self.monsters[6].published_date = timezone.now() + timedelta(days=6)
        self.monsters[6].save()
        self.monsters[7].published_date = timezone.now() + timedelta(days=7)
        self.monsters[7].save()
        self.monsters[8].published_date = timezone.now() + timedelta(days=8)
        self.monsters[8].save()
        self.monsters[9].published_date = timezone.now() + timedelta(days=9)
        self.monsters[9].save()
        self.monsters[10].published_date = timezone.now() + timedelta(days=10)
        self.monsters[10].save()
        self.monsters[11].published_date = timezone.now() + timedelta(days=11)
        self.monsters[11].save()
        self.monsters[12].published_date = timezone.now() + timedelta(days=12)
        self.monsters[12].save()
        self.monsters[13].published_date = timezone.now() + timedelta(days=13)
        self.monsters[13].save()
        self.monsters[14].published_date = timezone.now() + timedelta(days=14)
        self.monsters[14].save()

        self.npcs = mommy.make(
            NPC,
            user=self.users[0],
            is_published=True,
            _quantity=15,
            _fill_optional=True,
        )
        self.npcs[0].published_date = timezone.now()
        self.npcs[0].save()
        self.npcs[1].published_date = timezone.now() + timedelta(days=1)
        self.npcs[1].save()
        self.npcs[2].published_date = timezone.now() + timedelta(days=2)
        self.npcs[2].save()
        self.npcs[3].published_date = timezone.now() + timedelta(days=3)
        self.npcs[3].save()
        self.npcs[4].published_date = timezone.now() + timedelta(days=4)
        self.npcs[4].save()
        self.npcs[5].published_date = timezone.now() + timedelta(days=5)
        self.npcs[5].save()
        self.npcs[6].published_date = timezone.now() + timedelta(days=6)
        self.npcs[6].save()
        self.npcs[7].published_date = timezone.now() + timedelta(days=7)
        self.npcs[7].save()
        self.npcs[8].published_date = timezone.now() + timedelta(days=8)
        self.npcs[8].save()
        self.npcs[9].published_date = timezone.now() + timedelta(days=9)
        self.npcs[9].save()
        self.npcs[10].published_date = timezone.now() + timedelta(days=10)
        self.npcs[10].save()
        self.npcs[11].published_date = timezone.now() + timedelta(days=11)
        self.npcs[11].save()
        self.npcs[12].published_date = timezone.now() + timedelta(days=12)
        self.npcs[12].save()
        self.npcs[13].published_date = timezone.now() + timedelta(days=13)
        self.npcs[13].save()
        self.npcs[14].published_date = timezone.now() + timedelta(days=14)
        self.npcs[14].save()

        self.players = mommy.make(
            Player,
            user=self.users[0],
            is_published=True,
            _quantity=15,
            _fill_optional=True,
        )
        self.players[0].published_date = timezone.now()
        self.players[0].save()
        self.players[1].published_date = timezone.now() + timedelta(days=1)
        self.players[1].save()
        self.players[2].published_date = timezone.now() + timedelta(days=2)
        self.players[2].save()
        self.players[3].published_date = timezone.now() + timedelta(days=3)
        self.players[3].save()
        self.players[4].published_date = timezone.now() + timedelta(days=4)
        self.players[4].save()
        self.players[5].published_date = timezone.now() + timedelta(days=5)
        self.players[5].save()
        self.players[6].published_date = timezone.now() + timedelta(days=6)
        self.players[6].save()
        self.players[7].published_date = timezone.now() + timedelta(days=7)
        self.players[7].save()
        self.players[8].published_date = timezone.now() + timedelta(days=8)
        self.players[8].save()
        self.players[9].published_date = timezone.now() + timedelta(days=9)
        self.players[9].save()
        self.players[10].published_date = timezone.now() + timedelta(days=10)
        self.players[10].save()
        self.players[11].published_date = timezone.now() + timedelta(days=11)
        self.players[11].save()
        self.players[12].published_date = timezone.now() + timedelta(days=12)
        self.players[12].save()
        self.players[13].published_date = timezone.now() + timedelta(days=13)
        self.players[13].save()
        self.players[14].published_date = timezone.now() + timedelta(days=14)
        self.players[14].save()

        self.reviews = mommy.make(
            Review,
            user=self.users[1],
            campaign=self.campaigns[0],
            monster=None,
            npc=None,
            player=None,
            score=0,
            _quantity=21,
            _fill_optional=True,
        )
        self.reviews[1].user = self.users[2]
        self.reviews[1].save()
        self.reviews[2].user = self.users[3]
        self.reviews[2].save()
        self.reviews[3].campaign = None
        self.reviews[3].monster = self.monsters[0]
        self.reviews[3].score = randint(1,5)
        self.reviews[3].save()
        self.reviews[4].campaign = None
        self.reviews[4].monster = self.monsters[1]
        self.reviews[4].score = randint(1,5)
        self.reviews[4].save()
        self.reviews[5].campaign = None
        self.reviews[5].monster = self.monsters[2]
        self.reviews[5].score = randint(1,5)
        self.reviews[5].save()
        self.reviews[6].campaign = None
        self.reviews[6].monster = self.monsters[3]
        self.reviews[6].score = randint(1,5)
        self.reviews[6].save()
        self.reviews[7].campaign = None
        self.reviews[7].monster = self.monsters[4]
        self.reviews[7].score = randint(1,5)
        self.reviews[7].save()
        self.reviews[8].campaign = None
        self.reviews[8].monster = self.monsters[4]
        self.reviews[8].score = randint(1,5)
        self.reviews[8].save()
        self.reviews[9].campaign = None
        self.reviews[9].npc = self.npcs[5]
        self.reviews[9].score = randint(1,5)
        self.reviews[9].save()
        self.reviews[10].campaign = None
        self.reviews[10].npc = self.npcs[6]
        self.reviews[10].score = randint(1,5)
        self.reviews[10].save()
        self.reviews[11].campaign = None
        self.reviews[11].npc = self.npcs[7]
        self.reviews[11].score = randint(1,5)
        self.reviews[11].save()
        self.reviews[12].campaign = None
        self.reviews[12].npc = self.npcs[8]
        self.reviews[12].score = randint(1,5)
        self.reviews[12].save()
        self.reviews[13].campaign = None
        self.reviews[13].npc = self.npcs[9]
        self.reviews[13].score = randint(1,5)
        self.reviews[13].save()
        self.reviews[14].campaign = None
        self.reviews[14].npc = self.npcs[9]
        self.reviews[14].score = randint(1,5)
        self.reviews[14].save()
        self.reviews[15].campaign = None
        self.reviews[15].player = self.players[0]
        self.reviews[15].score = randint(1,5)
        self.reviews[15].save()
        self.reviews[16].campaign = None
        self.reviews[16].player = self.players[1]
        self.reviews[16].score = randint(1,5)
        self.reviews[16].save()
        self.reviews[17].campaign = None
        self.reviews[17].player = self.players[2]
        self.reviews[17].score = randint(1,5)
        self.reviews[17].save()
        self.reviews[18].campaign = None
        self.reviews[18].player = self.players[3]
        self.reviews[18].score = randint(1,5)
        self.reviews[18].save()
        self.reviews[19].campaign = None
        self.reviews[19].player = self.players[4]
        self.reviews[19].score = randint(1,5)
        self.reviews[19].save()
        self.reviews[20].campaign = None
        self.reviews[20].player = self.players[4]
        self.reviews[20].score = randint(1,5)
        self.reviews[20].save()

    def test_tavern_page(self):
        response = self.client.get('/tavern/')
        self.assertRedirects(response, '/accounts/login/?next=/tavern/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Tavern")
        self.assertContains(response, self.campaigns[0].title)
        # monsters 0-4 have reviews, 5-9 don't, and 10-14 are the most recent
        self.assertContains(response, self.monsters[0].name)
        self.assertContains(response, self.monsters[1].name)
        self.assertContains(response, self.monsters[2].name)
        self.assertContains(response, self.monsters[3].name)
        self.assertContains(response, self.monsters[4].name)
        self.assertContains(response, self.monsters[14].name)
        self.assertContains(response, self.monsters[13].name)
        self.assertContains(response, self.monsters[12].name)
        self.assertContains(response, self.monsters[11].name)
        self.assertContains(response, self.monsters[10].name)
        self.assertNotContains(response, self.monsters[9].name)
        self.assertNotContains(response, self.monsters[8].name)
        self.assertNotContains(response, self.monsters[7].name)
        self.assertNotContains(response, self.monsters[6].name)
        self.assertNotContains(response, self.monsters[5].name)
        # npcs 5-9 have reviews, 0-4 don't, and 10-14 are the most recent
        self.assertContains(response, self.npcs[5].name)
        self.assertContains(response, self.npcs[6].name)
        self.assertContains(response, self.npcs[7].name)
        self.assertContains(response, self.npcs[8].name)
        self.assertContains(response, self.npcs[9].name)
        self.assertContains(response, self.npcs[14].name)
        self.assertContains(response, self.npcs[13].name)
        self.assertContains(response, self.npcs[12].name)
        self.assertContains(response, self.npcs[11].name)
        self.assertContains(response, self.npcs[10].name)
        self.assertNotContains(response, self.npcs[0].name)
        self.assertNotContains(response, self.npcs[1].name)
        self.assertNotContains(response, self.npcs[2].name)
        self.assertNotContains(response, self.npcs[3].name)
        self.assertNotContains(response, self.npcs[4].name)
        # players 0-4 have reviews, 5-9 don't, and 10-14 are the most recent
        self.assertContains(response, self.players[0].character_name)
        self.assertContains(response, self.players[1].character_name)
        self.assertContains(response, self.players[2].character_name)
        self.assertContains(response, self.players[3].character_name)
        self.assertContains(response, self.players[4].character_name)
        self.assertContains(response, self.players[14].character_name)
        self.assertContains(response, self.players[13].character_name)
        self.assertContains(response, self.players[12].character_name)
        self.assertContains(response, self.players[11].character_name)
        self.assertContains(response, self.players[10].character_name)
        self.assertNotContains(response, self.players[9].character_name)
        self.assertNotContains(response, self.players[8].character_name)
        self.assertNotContains(response, self.players[7].character_name)
        self.assertNotContains(response, self.players[6].character_name)
        self.assertNotContains(response, self.players[5].character_name)

    def test_tavern_campaign_page(self):
        response = self.client.get('/tavern/campaign/{}/'.format(self.campaigns[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/campaign/{}/'.format(self.campaigns[0].pk), 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaign/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.campaigns[0].tavern_description)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.reviews[0].comment)
        self.assertContains(response, self.reviews[1].comment)
        self.assertContains(response, self.reviews[2].comment)
        self.assertContains(response, "Import Campaign")
        self.assertNotContains(response, "Unpublish Campaign")
        self.assertContains(response, "Review Campaign")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/campaign/{}/'.format(self.campaigns[0].pk))
        self.assertContains(response, "Unpublish Campaign")
        self.assertNotContains(response, "Import Campaign")

    def test_tavern_campaign_import(self):
        response = self.client.get('/tavern/campaign/{}/import/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/campaign/{}/import/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaign/{}/import/'.format(self.campaigns[0].pk))
        campaigns = Campaign.objects.all().order_by('-pk')
        self.assertRedirects(response, '/campaign/{}/'.format(campaigns[0].pk), 302, 200)
        response = self.client.get('/campaign/{}/'.format(campaigns[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_tavern_campaign_review(self):
        response = self.client.get('/tavern/campaign/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/campaign/{}/review/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaign/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/tavern/campaign/{}/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/campaign/{}/review/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
            "You've already submitted a review for this Campaign")
        self.assertContains(response, "Review Campaign")
        comment = "This Campaign is great"
        data = {
            'score': 5,
            'comment': comment,
        }
        response = self.client.post(
            '/tavern/campaign/{}/review/'.format(self.campaigns[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/campaign/{}/'.format(self.campaigns[0].pk),
            302, 200)
        response = self.client.get('/tavern/campaign/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

    def test_tavern_character_page(self):
        response = self.client.get('/tavern/monster/{}/'.format(self.monsters[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/monster/{}/'.format(self.monsters[0].pk), 302, 200)

        response = self.client.get('/tavern/npc/{}/'.format(self.npcs[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/npc/{}/'.format(self.npcs[0].pk), 302, 200)

        response = self.client.get('/tavern/player/{}/'.format(self.players[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/player/{}/'.format(self.players[0].pk), 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/monster/{}/'.format(self.monsters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.monsters[0].name)
        self.assertContains(response, self.monsters[0].tavern_description)
        self.assertContains(response, self.reviews[3].comment)
        self.assertNotContains(response, self.reviews[4].comment)
        self.assertNotContains(response, self.reviews[5].comment)
        self.assertNotContains(response, self.reviews[6].comment)
        self.assertNotContains(response, self.reviews[7].comment)
        self.assertNotContains(response, self.reviews[8].comment)
        self.assertContains(response, "Import monster")
        self.assertNotContains(response, "Unpublish monster")
        self.assertContains(response, "Review monster")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/monster/{}/'.format(self.monsters[0].pk))
        self.assertContains(response, "Unpublish monster")
        self.assertNotContains(response, "Import monster")

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/npc/{}/'.format(self.npcs[5].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.npcs[5].name)
        self.assertContains(response, self.npcs[5].tavern_description)
        self.assertContains(response, self.reviews[9].comment)
        self.assertNotContains(response, self.reviews[10].comment)
        self.assertNotContains(response, self.reviews[11].comment)
        self.assertNotContains(response, self.reviews[12].comment)
        self.assertNotContains(response, self.reviews[13].comment)
        self.assertNotContains(response, self.reviews[14].comment)
        self.assertContains(response, "Import NPC")
        self.assertNotContains(response, "Unpublish NPC")
        self.assertContains(response, "Review NPC")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/npc/{}/'.format(self.npcs[5].pk))
        self.assertContains(response, "Unpublish NPC")
        self.assertNotContains(response, "Import NPC")

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/player/{}/'.format(self.players[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].character_name)
        self.assertContains(response, self.players[0].tavern_description)
        self.assertContains(response, self.reviews[15].comment)
        self.assertNotContains(response, self.reviews[16].comment)
        self.assertNotContains(response, self.reviews[17].comment)
        self.assertNotContains(response, self.reviews[18].comment)
        self.assertNotContains(response, self.reviews[19].comment)
        self.assertNotContains(response, self.reviews[20].comment)
        self.assertContains(response, "Import player")
        self.assertNotContains(response, "Unpublish player")
        self.assertContains(response, "Review player")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/player/{}/'.format(self.players[0].pk))
        self.assertContains(response, "Unpublish player")
        self.assertNotContains(response, "Import player")

    def test_tavern_character_import(self):
        response = self.client.get('/tavern/monster/{}/import/'.format(self.monsters[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/monster/{}/import/'.format(self.monsters[0].pk),
            302, 200)

        response = self.client.get('/tavern/npc/{}/import/'.format(self.npcs[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/npc/{}/import/'.format(self.npcs[0].pk),
            302, 200)

        response = self.client.get('/tavern/player/{}/import/'.format(self.players[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/player/{}/import/'.format(self.players[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/monster/{}/import/'.format(self.monsters[0].pk))
        monsters = Monster.objects.all().order_by('-pk')
        self.assertRedirects(response, '/characters/monster/{}/'.format(monsters[0].pk), 302, 200)
        response = self.client.get('/characters/monster/{}/'.format(monsters[0].pk))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/npc/{}/import/'.format(self.npcs[0].pk))
        npcs = NPC.objects.all().order_by('-pk')
        self.assertRedirects(response, '/characters/npc/{}/'.format(npcs[0].pk), 302, 200)
        response = self.client.get('/characters/npc/{}/'.format(npcs[0].pk))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/player/{}/import/'.format(self.players[0].pk))
        players = Player.objects.all().order_by('-pk')
        self.assertRedirects(response, '/characters/player/{}/'.format(players[0].pk), 302, 200)
        response = self.client.get('/characters/player/{}/'.format(players[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_tavern_character_review(self):
        # unauthenticated users
        response = self.client.get('/tavern/monster/{}/review/'.format(self.monsters[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/monster/{}/review/'.format(self.monsters[0].pk),
            302, 200)

        response = self.client.get('/tavern/npc/{}/review/'.format(self.npcs[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/npc/{}/review/'.format(self.npcs[0].pk),
            302, 200)

        response = self.client.get('/tavern/player/{}/review/'.format(self.players[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/player/{}/review/'.format(self.players[0].pk),
            302, 200)

        # user has already submitted a review
        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/monster/{}/review/'.format(self.monsters[0].pk))
        self.assertRedirects(
            response,
            '/tavern/monster/{}/'.format(self.monsters[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/npc/{}/review/'.format(self.npcs[5].pk))
        self.assertRedirects(
            response,
            '/tavern/npc/{}/'.format(self.npcs[5].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/player/{}/review/'.format(self.players[0].pk))
        self.assertRedirects(
            response,
            '/tavern/player/{}/'.format(self.players[0].pk),
            302, 200)

        # submitting a new review
        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/monster/{}/review/'.format(self.monsters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
            "You've already submitted a review")
        self.assertContains(response, "Review character")
        comment = "This is great"
        data = {
            'score': 5,
            'comment': comment,
        }
        response = self.client.post(
            '/tavern/monster/{}/review/'.format(self.monsters[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/monster/{}/'.format(self.monsters[0].pk),
            302, 200)
        response = self.client.get('/tavern/monster/{}/'.format(self.monsters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/npc/{}/review/'.format(self.npcs[5].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
            "You've already submitted a review")
        self.assertContains(response, "Review character")
        comment = "This is great"
        data = {
            'score': 5,
            'comment': comment,
        }
        response = self.client.post(
            '/tavern/npc/{}/review/'.format(self.npcs[5].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/npc/{}/'.format(self.npcs[5].pk),
            302, 200)
        response = self.client.get('/tavern/npc/{}/'.format(self.npcs[5].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/player/{}/review/'.format(self.players[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
            "You've already submitted a review")
        self.assertContains(response, "Review character")
        comment = "This is great"
        data = {
            'score': 5,
            'comment': comment,
        }
        response = self.client.post(
            '/tavern/player/{}/review/'.format(self.players[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/player/{}/'.format(self.players[0].pk),
            302, 200)
        response = self.client.get('/tavern/player/{}/'.format(self.players[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)
