from django.contrib.auth.models import User
from django.test import Client, TestCase

import unittest

from model_mommy import mommy

from campaign.models import Campaign, Chapter, Section
from tavern.models import Review


class CampaignTest(TestCase):
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

        self.reviews = mommy.make(
            Review,
            user=self.users[1],
            campaign=self.campaigns[0],
            _quantity=3,
            _fill_optional=True,
        )
        self.reviews[1].user = self.users[2]
        self.reviews[1].save()
        self.reviews[2].user = self.users[3]
        self.reviews[2].save()

    def test_tavern_page(self):
        response = self.client.get('/tavern/')
        self.assertRedirects(response, '/accounts/login/?next=/tavern/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Tavern")
        self.assertContains(response, self.campaigns[0].title)

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