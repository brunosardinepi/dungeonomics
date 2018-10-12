from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from model_mommy import mommy

from . import forms
from . import models
from characters.models import Player
from posts.models import Post


class CampaignTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=5)

        self.campaigns = mommy.make(
            models.Campaign,
            user=self.users[0],
            is_published=True,
            _quantity=2,
            _fill_optional=True,
        )
        self.campaigns[1].user = self.users[1]
        self.campaigns[1].is_published = False
        self.campaigns[1].save()

        self.chapters = mommy.make(
            models.Chapter,
            user=self.users[0],
            campaign=self.campaigns[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.chapters[1].user = self.users[1]
        self.chapters[1].campaign = self.campaigns[1]
        self.chapters[1].save()

        self.sections = mommy.make(
            models.Section,
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

        self.players = mommy.make(
            Player,
            _quantity=3,
            user=self.users[1],
            _fill_optional=True,
        )
        self.players[1].campaigns.add(self.campaigns[0])
        self.players[2].campaigns.add(self.campaigns[0])

        self.post = mommy.make(
            Post,
            user=self.users[0],
            campaign=self.campaigns[0],
            _fill_optional=True,
        )

        self.reviews = mommy.make(
            models.Review,
            user=self.users[1],
            campaign=self.campaigns[0],
            _quantity=3,
            _fill_optional=True,
        )
        self.reviews[1].user = self.users[2]
        self.reviews[1].save()
        self.reviews[2].user = self.users[3]
        self.reviews[2].save()

    def test_campaign_creation_time(self):
        campaign = models.Campaign.objects.create(
            user=self.users[0],
            title="test campaign time",
        )
        now = timezone.now()
        self.assertLess(campaign.created_at, now)

    def test_unique_public_url(self):
        campaign = models.Campaign.objects.create(
            user=self.users[0],
            title="testing uuid",
        )
        check = models.Campaign.objects.filter(public_url=campaign.public_url)
        self.assertEqual(check.count(), 1)

    def test_campaign_exists(self):
        campaigns = models.Campaign.objects.all()

        self.assertIn(self.campaigns[0], campaigns)
        self.assertIn(self.campaigns[1], campaigns)

    def test_chapter_exists(self):
        chapters = models.Chapter.objects.all()

        self.assertIn(self.chapters[0], chapters)
        self.assertIn(self.chapters[1], chapters)

    def test_section_exists(self):
        sections = models.Section.objects.all()

        self.assertIn(self.sections[0], sections)
        self.assertIn(self.sections[1], sections)

    def test_campaign_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.chapters[0].content)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_campaign_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaigns[1].pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test campaign title'
        }
        response = self.client.post('/campaign/create/', data)

        campaign = models.Campaign.objects.get(title='test campaign title')
        self.assertRedirects(response, '/campaign/{}/'.format(campaign.pk), 302, 200)

        response = self.client.get('/campaign/{}/'.format(campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test campaign title')

    def test_campaign_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/edit/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)

    def test_campaign_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test campaign title EDIT',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.chapters[0].pk,
            'form-0-order': 1,
            'form-0-title': self.chapters[0].title,
        }
        response = self.client.post('/campaign/{}/edit/'.format(self.campaigns[0].pk), data)
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaigns[0].pk), 302, 200)

        response = self.client.get('/campaign/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test campaign title EDIT')

    def test_campaign_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/delete/'.format(self.campaigns[0].pk), {})
        self.assertRedirects(response, '/', 302, 200)

        campaigns = models.Campaign.objects.all()
        self.assertNotIn(self.campaigns[0], campaigns)
        self.assertEqual(campaigns.count(), 1)

    def test_campaign_print_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/print/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.chapters[0].content)

    def test_campaign_export_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/print/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.chapters[0].content)

    def test_chapter_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.chapters[0].content)

    def test_chapter_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaigns[1].pk, self.chapters[1].pk))

        self.assertEqual(response.status_code, 404)

    def test_chapter_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test chapter title',
            'content': 'zzzzzzzzzz',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/create/'.format(self.campaigns[0].pk), data)

        chapter = models.Chapter.objects.get(title='test chapter title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, chapter.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, chapter.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title')

    def test_chapter_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/edit/'.format(self.campaigns[0].pk, self.chapters[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.chapters[0].content)
        self.assertContains(response, self.chapters[0].order)
        sections = models.Section.objects.filter(chapter=self.chapters[0])
        for section in sections:
            self.assertContains(response, section.title)

    def test_chapter_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test chapter title EDIT',
            'content': 'zzzzzzzzzz EDIT',
            'order': '2',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.sections[0].pk,
            'form-0-order': 1,
            'form-0-title': self.sections[0].title,
        }
        response = self.client.post('/campaign/{}/chapter/{}/edit/'.format(self.campaigns[0].pk, self.chapters[0].pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title EDIT')

    def test_chapter_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/chapter/{}/delete/'.format(self.campaigns[0].pk, self.chapters[0].pk), {})
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaigns[0].pk), 302, 200)

        chapters = models.Chapter.objects.all()
        self.assertNotIn(self.chapters[0], chapters)
        self.assertEqual(chapters.count(), 1)

    def test_section_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.sections[0].content)

    def test_section_page_bad_user(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[1].pk, self.chapters[1].pk, self.sections[1].pk))

        self.assertEqual(response.status_code, 404)

    def test_section_create(self):
        self.client.force_login(self.users[0])

        data = {
            'title': 'test section title',
            'content': 'yyyyyyyyyyyyy',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/create/'.format(self.campaigns[0].pk, self.chapters[0].pk), data)

        section = models.Section.objects.get(title='test section title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk, section.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk, section.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title')

    def test_section_edit_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.chapters[0].title)
        self.assertContains(response, self.sections[0].title)
        self.assertContains(response, self.sections[0].content)
        self.assertContains(response, self.sections[0].order)

    def test_section_edit(self):
        self.client.force_login(self.users[0])
        data = {
            'title': 'test section title EDIT',
            'content': 'xxxxxxxxxxxxx EDIT',
            'order': '2',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title EDIT')

    def test_section_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/delete/'.format(self.campaigns[0].pk, self.chapters[0].pk, self.sections[0].pk), {})
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaigns[0].pk, self.chapters[0].pk), 302, 200)

        sections = models.Section.objects.all()
        self.assertNotIn(self.sections[0], sections)
        self.assertEqual(sections.count(), 1)

    def test_campaign_party_page(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[1].player_name)
        self.assertContains(response, self.players[1].character_name)
        self.assertContains(response, self.players[2].player_name)
        self.assertContains(response, self.players[2].character_name)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_campaign_party_invite_page_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/invite/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.campaigns[0].public_url)

    def test_campaign_party_invite_accept_page_players(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/'.format(self.campaigns[0].public_url))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_campaign_party_invite_accept_page_no_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/'.format(self.campaigns[0].public_url))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[0].title)
        self.assertContains(response, "You haven't created any Players")

    def test_campaign_party_invite_accept_page_no_auth_no_invite(self):
        response = self.client.get('/campaign/{}/'.format(self.campaigns[0].public_url))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/'.format(self.campaigns[0].public_url), 302, 200)

    def test_campaign_party_invite(self):
        self.client.force_login(self.users[1])
        response = self.client.post('/campaign/{}/'.format(self.campaigns[0].public_url), {'player': self.players[0].pk})
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaigns[0].pk), 302, 200)

        players = self.campaigns[0].player_set.all()
        self.assertEqual(players.count(), 3)

        response = self.client.get('/campaign/{}/party/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)

    def test_campaign_party_remove_page_players(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[1].player_name)
        self.assertContains(response, self.players[1].character_name)
        self.assertContains(response, self.players[2].player_name)
        self.assertContains(response, self.players[2].character_name)

    def test_campaign_party_remove_page_no_players(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaigns[1].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Campaign doesn't have any Players")

    def test_campaign_party_remove_page_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaigns[1].pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_party_remove_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/remove/'.format(self.campaigns[1].pk))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/remove/'.format(self.campaigns[1].pk), 302, 200)

    def test_campaign_party_remove(self):
        players = self.campaigns[0].player_set.all()
        self.assertEqual(players.count(), 2)

        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/party/remove/'.format(self.campaigns[0].pk), {'players': [self.players[1].pk, self.players[2].pk]})
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaigns[0].pk), 302, 200)

        players = self.campaigns[0].player_set.all()
        self.assertEqual(players.count(), 0)

        response = self.client.get('/campaign/{}/party/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[2].player_name)
        self.assertNotContains(response, self.players[2].character_name)
        self.assertContains(response, "You haven't invited anyone to your party")

    def test_campaign_party_player_detail_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaigns[0].pk, self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)

    def test_campaign_party_player_detail_player(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaigns[0].pk, self.players[0].pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.players[0].player_name)
        self.assertContains(response, self.players[0].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)
        self.assertNotContains(response, self.players[1].player_name)
        self.assertNotContains(response, self.players[1].character_name)

    def test_campaign_party_player_detail_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaigns[0].pk, self.players[0].pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_party_player_detail_no_auth(self):
        response = self.client.get('/campaign/{}/party/players/{}/'.format(self.campaigns[0].pk, self.players[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/players/{}/'.format(self.campaigns[0].pk, self.players[0].pk), 302, 200)

    def test_tavern_page(self):
        response = self.client.get('/tavern/')
        self.assertRedirects(response, '/accounts/login/?next=/tavern/', 302, 200)

        self.client.force_login(self.users[0])
        response = self.client.get('/tavern/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Tavern")
        self.assertContains(response, self.campaigns[0].title)

    def test_tavern_campaign_page(self):
        response = self.client.get('/tavern/{}/'.format(self.campaigns[0].pk))
        self.assertRedirects(response, '/accounts/login/?next=/tavern/{}/'.format(self.campaigns[0].pk), 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/{}/'.format(self.campaigns[0].pk))
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
        response = self.client.get('/tavern/{}/'.format(self.campaigns[0].pk))
        self.assertContains(response, "Unpublish Campaign")
        self.assertNotContains(response, "Import Campaign")

    def test_tavern_import(self):
        response = self.client.get('/tavern/{}/import/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/{}/import/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/{}/import/'.format(self.campaigns[0].pk))
        campaigns = models.Campaign.objects.all().order_by('-pk')
        self.assertRedirects(response, '/campaign/{}/'.format(campaigns[0].pk), 302, 200)
        response = self.client.get('/campaign/{}/'.format(campaigns[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_tavern_review(self):
        response = self.client.get('/tavern/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/tavern/{}/review/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/tavern/{}/review/'.format(self.campaigns[0].pk))
        self.assertRedirects(
            response,
            '/tavern/{}/'.format(self.campaigns[0].pk),
            302, 200)

        self.client.force_login(self.users[4])
        response = self.client.get('/tavern/{}/review/'.format(self.campaigns[0].pk))
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
            '/tavern/{}/review/'.format(self.campaigns[0].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/{}/'.format(self.campaigns[0].pk),
            302, 200)
        response = self.client.get('/tavern/{}/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment)

    def test_tavern_publish(self):
        response = self.client.get('/campaign/{}/publish/'.format(self.campaigns[1].pk))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/campaign/{}/publish/'.format(self.campaigns[1].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/publish/'.format(self.campaigns[1].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publish Campaign")
        tavern_description = "Please don't hate my Campaign"
        data = {
            'tavern_description': tavern_description,
        }
        response = self.client.post(
            '/campaign/{}/publish/'.format(self.campaigns[1].pk),
            data,
        )
        self.assertRedirects(
            response,
            '/tavern/{}/'.format(self.campaigns[1].pk),
            302, 200)
        response = self.client.get('/tavern/{}/'.format(self.campaigns[1].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaigns[1].title)
        self.assertContains(response, tavern_description)