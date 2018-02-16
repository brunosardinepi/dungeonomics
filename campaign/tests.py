from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from . import forms
from . import models


class CampaignTest(TestCase):
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

        self.campaign = models.Campaign.objects.create(
            user=self.user,
            title="test campaign",
        )

        self.chapter = models.Chapter.objects.create(
            user=self.user,
            title="test chapter",
            campaign=self.campaign,
            content="aaaaaaaaaa",
        )

        self.section = models.Section.objects.create(
            user=self.user,
            title="test section",
            chapter=self.chapter,
            campaign=self.campaign,
            content="bbbbbbbbbb",
        )

        self.campaign2 = models.Campaign.objects.create(
            user=self.user2,
            title="test campaign 2",
        )

        self.chapter2 = models.Chapter.objects.create(
            user=self.user2,
            title="test chapter 2",
            campaign=self.campaign2,
            content="cccccccccc",
        )

        self.section2 = models.Section.objects.create(
            user=self.user2,
            title="test section 2",
            chapter=self.chapter2,
            campaign=self.campaign2,
            content="dddddddddd",
        )

    def test_campaign_creation_time(self):
        campaign = models.Campaign.objects.create(
            user=self.user,
            title="test campaign time",
        )
        now = timezone.now()
        self.assertLess(campaign.created_at, now)

    def test_campaign_exists(self):
        campaigns = models.Campaign.objects.all()

        self.assertIn(self.campaign, campaigns)
        self.assertIn(self.campaign2, campaigns)

    def test_chapter_exists(self):
        chapters = models.Chapter.objects.all()

        self.assertIn(self.chapter, chapters)
        self.assertIn(self.chapter2, chapters)

    def test_section_exists(self):
        sections = models.Section.objects.all()

        self.assertIn(self.section, sections)
        self.assertIn(self.section2, sections)

    def test_campaign_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)

    def test_campaign_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/'.format(self.campaign2.pk))

        self.assertEqual(response.status_code, 404)

    def test_campaign_create(self):
        self.client.login(username='testuser', password='testpassword')

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
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/edit/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)

    def test_campaign_edit(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'title': 'test campaign title EDIT',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.chapter.pk,
            'form-0-order': 1,
            'form-0-title': self.chapter.title,
        }
        response = self.client.post('/campaign/{}/edit/'.format(self.campaign.pk), data)
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaign.pk), 302, 200)

        response = self.client.get('/campaign/{}/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test campaign title EDIT')

    def test_campaign_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/delete/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)

    def test_campaign_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/campaign/{}/delete/'.format(self.campaign.pk), {})
        self.assertRedirects(response, '/', 302, 200)

        campaigns = models.Campaign.objects.all()
        self.assertNotIn(self.campaign, campaigns)
        self.assertEqual(campaigns.count(), 1)

    def test_campaign_print_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/print/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)

    def test_campaign_export_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/print/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.chapter.content)

    def test_chapter_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.chapter.content)

    def test_chapter_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign2.pk, self.chapter2.pk))

        self.assertEqual(response.status_code, 404)

    def test_chapter_create(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'title': 'test chapter title',
            'content': 'zzzzzzzzzz',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/create/'.format(self.campaign.pk), data)

        chapter = models.Chapter.objects.get(title='test chapter title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, chapter.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, chapter.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title')

    def test_chapter_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/edit/'.format(self.campaign.pk, self.chapter.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.chapter.content)
        self.assertContains(response, self.chapter.order)
        sections = models.Section.objects.filter(chapter=self.chapter)
        for section in sections:
            self.assertContains(response, section.title)

    def test_chapter_edit(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'title': 'test chapter title EDIT',
            'content': 'zzzzzzzzzz EDIT',
            'order': '2',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': self.section.pk,
            'form-0-order': 1,
            'form-0-title': self.section.title,
        }
        response = self.client.post('/campaign/{}/chapter/{}/edit/'.format(self.campaign.pk, self.chapter.pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test chapter title EDIT')

    def test_chapter_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/delete/'.format(self.campaign.pk, self.chapter.pk))
        self.assertEqual(response.status_code, 200)

    def test_chapter_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/campaign/{}/chapter/{}/delete/'.format(self.campaign.pk, self.chapter.pk), {})
        self.assertRedirects(response, '/campaign/{}/'.format(self.campaign.pk), 302, 200)

        chapters = models.Chapter.objects.all()
        self.assertNotIn(self.chapter, chapters)
        self.assertEqual(chapters.count(), 1)

    def test_section_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.section.content)

    def test_section_page_bad_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign2.pk, self.chapter2.pk, self.section2.pk))

        self.assertEqual(response.status_code, 404)

    def test_section_create(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'title': 'test section title',
            'content': 'yyyyyyyyyyyyy',
            'order': '1',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/create/'.format(self.campaign.pk, self.chapter.pk), data)

        section = models.Section.objects.get(title='test section title')
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, section.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, section.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title')

    def test_section_edit_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.campaign.title)
        self.assertContains(response, self.chapter.title)
        self.assertContains(response, self.section.title)
        self.assertContains(response, self.section.content)
        self.assertContains(response, self.section.order)

    def test_section_edit(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'title': 'test section title EDIT',
            'content': 'xxxxxxxxxxxxx EDIT',
            'order': '2',
        }
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/edit/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), data)
        self.assertRedirects(response, '/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), 302, 200)

        response = self.client.get('/campaign/{}/chapter/{}/section/{}/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test section title EDIT')

    def test_section_delete_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/chapter/{}/section/{}/delete/'.format(self.campaign.pk, self.chapter.pk, self.section.pk))
        self.assertEqual(response.status_code, 200)

    def test_section_delete(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/campaign/{}/chapter/{}/section/{}/delete/'.format(self.campaign.pk, self.chapter.pk, self.section.pk), {})
        self.assertRedirects(response, '/campaign/{}/chapter/{}/'.format(self.campaign.pk, self.chapter.pk), 302, 200)

        sections = models.Section.objects.all()
        self.assertNotIn(self.section, sections)
        self.assertEqual(sections.count(), 1)