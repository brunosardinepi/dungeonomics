from datetime import timedelta
from random import randint

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from model_mommy import mommy

from campaign.models import Campaign, Chapter, Section
from characters.models import GeneralCharacter
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

        self.characters = mommy.make(
            GeneralCharacter,
            user=self.users[0],
            is_published=True,
            _quantity=15,
            _fill_optional=True,
        )
        self.characters[0].published_date = timezone.now()
        self.characters[0].save()
        self.characters[1].published_date = timezone.now() + timedelta(days=1)
        self.characters[1].save()
        self.characters[2].published_date = timezone.now() + timedelta(days=2)
        self.characters[2].save()
        self.characters[3].published_date = timezone.now() + timedelta(days=3)
        self.characters[3].save()
        self.characters[4].published_date = timezone.now() + timedelta(days=4)
        self.characters[4].save()
        self.characters[5].published_date = timezone.now() + timedelta(days=5)
        self.characters[5].save()
        self.characters[6].published_date = timezone.now() + timedelta(days=6)
        self.characters[6].save()
        self.characters[7].published_date = timezone.now() + timedelta(days=7)
        self.characters[7].save()
        self.characters[8].published_date = timezone.now() + timedelta(days=8)
        self.characters[8].save()
        self.characters[9].published_date = timezone.now() + timedelta(days=9)
        self.characters[9].save()
        self.characters[10].published_date = timezone.now() + timedelta(days=10)
        self.characters[10].save()
        self.characters[11].published_date = timezone.now() + timedelta(days=11)
        self.characters[11].save()
        self.characters[12].published_date = timezone.now() + timedelta(days=12)
        self.characters[12].save()
        self.characters[13].published_date = timezone.now() + timedelta(days=13)
        self.characters[13].save()
        self.characters[14].published_date = timezone.now() + timedelta(days=14)
        self.characters[14].save()

        self.reviews = mommy.make(
            Review,
            user=self.users[1],
            campaign=self.campaigns[0],
            character=None,
            score=0,
            _quantity=9,
            _fill_optional=True,
        )
        self.reviews[1].user = self.users[2]
        self.reviews[1].save()
        self.reviews[2].user = self.users[3]
        self.reviews[2].save()
        self.reviews[3].campaign = None
        self.reviews[3].character = self.characters[0]
        self.reviews[3].score = randint(1,5)
        self.reviews[3].save()
        self.reviews[4].campaign = None
        self.reviews[4].character = self.characters[1]
        self.reviews[4].score = randint(1,5)
        self.reviews[4].save()
        self.reviews[5].campaign = None
        self.reviews[5].character = self.characters[2]
        self.reviews[5].score = randint(1,5)
        self.reviews[5].save()
        self.reviews[6].campaign = None
        self.reviews[6].character = self.characters[3]
        self.reviews[6].score = randint(1,5)
        self.reviews[6].save()
        self.reviews[7].campaign = None
        self.reviews[7].character = self.characters[4]
        self.reviews[7].score = randint(1,5)
        self.reviews[7].save()
        self.reviews[8].campaign = None
        self.reviews[8].character = self.characters[4]
        self.reviews[8].score = randint(1,5)
        self.reviews[8].save()

    def test_tavern_page(self):
        response = self.client.get('/tavern/')
        self.assertRedirects(response, '/accounts/login/?next=/tavern/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Tavern")
        self.assertContains(response, self.campaigns[0].title)
        # characters 0-4 have reviews, 5-9 don't, and 10-14 are the most recent
        self.assertContains(response, self.characters[0].name)
        self.assertContains(response, self.characters[1].name)
        self.assertContains(response, self.characters[2].name)
        self.assertContains(response, self.characters[3].name)
        self.assertContains(response, self.characters[4].name)
        self.assertContains(response, self.characters[14].name)
        self.assertContains(response, self.characters[13].name)
        self.assertContains(response, self.characters[12].name)
        self.assertContains(response, self.characters[11].name)
        self.assertContains(response, self.characters[10].name)
        self.assertNotContains(response, self.characters[9].name)
        self.assertNotContains(response, self.characters[8].name)
        self.assertNotContains(response, self.characters[7].name)
        self.assertNotContains(response, self.characters[6].name)
        self.assertNotContains(response, self.characters[5].name)

    def test_tavern_campaign_page(self):
        response = self.client.get('/tavern/campaigns/{}/'.format(self.campaigns[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/campaigns/{}/'.format(self.campaigns[0].pk), 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaigns/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.campaigns[0].tavern_description)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.reviews[0].comment)
        self.assertContains(response, self.reviews[1].comment)
        self.assertContains(response, self.reviews[2].comment)
        self.assertContains(response, "Import campaign")
        self.assertNotContains(response, "Unpublish campaign")
        self.assertContains(response, "Review campaign")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/campaigns/{}/'.format(self.campaigns[0].pk))
        self.assertContains(response, "Unpublish campaign")
        self.assertContains(response, "Import campaign", count=1)

    def test_tavern_campaign_import(self):
        response = self.client.get('/tavern/campaigns/{}/import/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/campaigns/{}/import/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaigns/{}/import/'.format(self.campaigns[0].pk))
        campaigns = Campaign.objects.all().order_by('-pk')
        self.assertRedirects(response, '/campaign/{}/'.format(campaigns[0].pk), 302, 200)
        response = self.client.get('/campaign/{}/'.format(campaigns[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_tavern_campaign_review(self):
        response = self.client.get('/tavern/campaigns/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/campaigns/{}/review/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/campaigns/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/tavern/campaigns/{}/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/campaigns/{}/review/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response,
            "You've already submitted a review for this campaign")
        self.assertContains(response, "Review campaign")
        comment = "This campaign is great"
        data = {
            'score': 5,
            'comment': comment,
        }
        response = self.client.post(
            '/tavern/campaigns/{}/review/'.format(self.campaigns[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/campaigns/{}/'.format(self.campaigns[0].pk),
            302, 200)
        response = self.client.get('/tavern/campaigns/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

    def test_tavern_character_page(self):
        response = self.client.get('/tavern/characters/{}/'.format(self.characters[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/characters/{}/'.format(self.characters[0].pk), 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/characters/{}/'.format(self.characters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.characters[0].name)
        self.assertContains(response, self.characters[0].tavern_description)
        self.assertContains(response, self.reviews[3].comment)
        self.assertNotContains(response, self.reviews[4].comment)
        self.assertNotContains(response, self.reviews[5].comment)
        self.assertNotContains(response, self.reviews[6].comment)
        self.assertNotContains(response, self.reviews[7].comment)
        self.assertNotContains(response, self.reviews[8].comment)
        self.assertContains(response, "Import character")
        self.assertNotContains(response, "Unpublish character")
        self.assertContains(response, "Review character")

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/characters/{}/'.format(self.characters[0].pk))
        self.assertContains(response, "Unpublish character")
        self.assertNotContains(response, "Import character")

    def test_tavern_character_import(self):
        response = self.client.get('/tavern/characters/{}/import/'.format(self.characters[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/characters/{}/import/'.format(self.characters[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/characters/{}/import/'.format(self.characters[0].pk))
        characters = GeneralCharacter.objects.all().order_by('-pk')
        self.assertRedirects(response, '/characters/{}/'.format(characters[0].pk), 302, 200)
        response = self.client.get('/characters/{}/'.format(characters[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_tavern_character_review(self):
        # unauthenticated users
        response = self.client.get('/tavern/characters/{}/review/'.format(self.characters[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/characters/{}/review/'.format(self.characters[0].pk),
            302, 200)

        # user has already submitted a review
        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/characters/{}/review/'.format(self.characters[0].pk))
        self.assertRedirects(
            response,
            '/tavern/characters/{}/'.format(self.characters[0].pk),
            302, 200)

        # submitting a new review
        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/characters/{}/review/'.format(self.characters[0].pk))
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
            '/tavern/characters/{}/review/'.format(self.characters[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/characters/{}/'.format(self.characters[0].pk),
            302, 200)
        response = self.client.get('/tavern/characters/{}/'.format(self.characters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

    def test_tavern_search(self):
        types = [
            "campaigns",
            "characters",
        ]

        # unauthenticated user
        for type in types:
            response = self.client.get('/tavern/search/{}/'.format(type))
            self.assertRedirects(response,
                '/accounts/login/?next=/tavern/search/{}/'.format(type),
                302, 200)

        # authenticated user
        self.client.force_login(self.users[0])

        for type in types:
            response = self.client.get('/tavern/search/{}/'.format(type))
            self.assertEqual(response.status_code, 200)

            if type == "campaigns":
                results = self.campaigns
            elif type == "characters":
                results = self.characters

            for result in results:
                if result.is_published == True:
                    self.assertContains(response, result)
