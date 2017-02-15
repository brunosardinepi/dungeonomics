from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.utils import timezone

import unittest

from . import forms
from . import models
from . import views


class CampaignTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        # create a test user
        self.user = User.objects.create_user(username='testuser', email='test@test.test', password='testpassword')

        # create a test user
        self.user2 = User.objects.create_user(username='testuser2', email='test2@test.test', password='testpassword')

        # create a test campaign for testuser
        self.campaign = models.Campaign.objects.create(
            user=self.user,
            title="test campaign"
        )

        # create a test chapter for test campaign
        self.chapter = models.Chapter.objects.create(
            user=self.user,
            title="test chapter",
            campaign=self.campaign,
            content="aaaaaaaaaa",
        )

        # create a test section for test chapter
        self.section = models.Section.objects.create(
            user=self.user,
            title="test section",
            chapter=self.chapter,
            campaign=self.campaign,
            content="bbbbbbbbbb",
        )

        # create a test campaign for testuser2
        self.campaign2 = models.Campaign.objects.create(
            user=self.user2,
            title="test campaign 2"
        )

        # create a test chapter for test campaign 2
        self.chapter2 = models.Chapter.objects.create(
            user=self.user2,
            title="test chapter 2",
            campaign=self.campaign2,
            content="cccccccccc",
        )

        # create a test section for test chapter 2
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
            title="test campaign time"
        )
        now = timezone.now()
        self.assertLess(campaign.created_at, now)

    def test_campaign_exists(self):
        """
        Test campaigns exist
        """

        # get queryset that contains all campaigns
        campaigns = models.Campaign.objects.all()

        # make sure the test campaigns exist in the queryset
        self.assertIn(self.campaign, campaigns)
        self.assertIn(self.campaign2, campaigns)

    def test_chapter_exists(self):
        """
        Test chapters exist
        """

        # get queryset that contains all chapters
        chapters = models.Chapter.objects.all()

        # make sure the test chapters exist in the queryset
        self.assertIn(self.chapter, chapters)
        self.assertIn(self.chapter2, chapters)

    def test_section_exists(self):
        """
        Test section exists
        """

        # get queryset that contains all sections
        sections = models.Section.objects.all()

        # make sure the test sections exist in the queryset
        self.assertIn(self.section, sections)
        self.assertIn(self.section2, sections)

    def test_campaign_page(self):
        """
        Campaign page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign.pk)

        # make sure the campaign information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.section.title, status_code=200)
        self.assertContains(response, self.chapter.content, status_code=200)

    @unittest.expectedFailure
    def test_campaign_page_bad_user(self):
        """
        Campaign page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign2.pk)

    def test_campaign_create(self):
        """
        Create campaign
        """

        form_data = {'title': 'test campaign title'}
        form = forms.CampaignForm(data=form_data)
        new_campaign = form.save(commit=False)
        new_campaign.user = self.user
        new_campaign.save()

        new_campaign = models.Campaign.objects.get(pk=new_campaign.pk)
        campaigns = models.Campaign.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_campaign, campaigns)

    def test_campaign_edit_page(self):
        """
        Edit campaign page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_update(request, self.campaign.pk)

        # make sure the campaign information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)

    def test_campaign_edit(self):
        """
        Edit campaign
        """

        form_data = {'title': 'test campaign title EDIT'}
        form = forms.CampaignForm(data=form_data)
        new_campaign = form.save(commit=False)
        new_campaign.user = self.user
        new_campaign.save()

        new_campaign = models.Campaign.objects.get(title="test campaign title EDIT")
        campaigns = models.Campaign.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_campaign, campaigns)

    def test_campaign_delete_page(self):
        """
        Delete campaign page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_delete(request, self.campaign.pk)

        # make sure the campaign information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)

    def test_campaign_delete(self):
        """
        Delete campaign
        """

        form_data = {'title': 'test campaign title'}
        form = forms.DeleteCampaignForm(data=form_data)
        new_campaign = form.save(commit=False)
        new_campaign.user = self.user
        new_campaign.save()

        self.assertTrue(form.is_valid())

    def test_campaign_print_page(self):
        """
        Print campaign page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_print(request, self.campaign.pk)

        # make sure the campaign information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.section.title, status_code=200)
        self.assertContains(response, self.chapter.content, status_code=200)

    def test_campaign_export_page(self):
        """
        Export campaign page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_export(request, self.campaign.pk)

        # make sure the campaign information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.section.title, status_code=200)
        self.assertContains(response, self.chapter.content, status_code=200)

    def test_chapter_page(self):
        """
        Chapter page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign.pk, self.chapter.pk)

        # make sure the chapter information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.chapter.content, status_code=200)

    @unittest.expectedFailure
    def test_chapter_page_bad_user(self):
        """
        Chapter page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign2.pk, self.chapter2.pk)

    def test_chapter_create_page(self):
        """
        Create chapter page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.chapter_create(request, self.campaign.pk)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_chapter_create(self):
        """
        Create chapter
        """

        form_data = {'title': 'test chapter title', 'content': 'zzzzzzzzzz', 'order': '1'}
        form = forms.ChapterForm(data=form_data)
        new_chapter = form.save(commit=False)
        new_chapter.campaign = self.campaign
        new_chapter.user = self.user
        new_chapter.save()

        new_chapter = models.Chapter.objects.get(pk=new_chapter.pk)
        chapters = models.Chapter.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_chapter, chapters)

    def test_chapter_edit_page(self):
        """
        Edit chapter page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.chapter_update(request, self.campaign.pk, self.chapter.pk)

        # make sure the chapter information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.chapter.content, status_code=200)
        self.assertContains(response, self.chapter.order, status_code=200)
        sections = models.Section.objects.filter(chapter=self.chapter)
        for section in sections:
            self.assertContains(response, section.title, status_code=200)

    def test_chapter_edit(self):
        """
        Edit chapter
        """

        form_data = {'title': 'test chapter title EDIT', 'content': 'zzzzzzzzzz EDIT', 'order': '2'}
        form = forms.ChapterForm(data=form_data)
        new_chapter = form.save(commit=False)
        new_chapter.campaign = self.campaign
        new_chapter.user = self.user
        new_chapter.save()

        new_chapter = models.Chapter.objects.get(title="test chapter title EDIT")
        chapters = models.Chapter.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_chapter, chapters)

    def test_chapter_delete_page(self):
        """
        Delete chapter page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.chapter_delete(request, self.chapter.campaign.pk, self.chapter.pk)

        # make sure the chapter information is on the page
        self.assertContains(response, self.chapter.title, status_code=200)

    def test_chapter_delete(self):
        """
        Delete chapter
        """

        form_data = {'title': 'test chapter title'}
        form = forms.DeleteChapterForm(data=form_data)
        new_chapter = form.save(commit=False)
        new_chapter.campaign = self.campaign
        new_chapter.user = self.user
        new_chapter.save()

        self.assertTrue(form.is_valid())

    def test_section_page(self):
        """
        Section page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign.pk, self.chapter.pk, self.section.pk)

        # make sure the section information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.section.title, status_code=200)
        self.assertContains(response, self.section.content, status_code=200)

    @unittest.expectedFailure
    def test_section_page_bad_user(self):
        """
        Section page is inaccessible by the wrong user
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.campaign_detail(request, self.campaign2.pk, self.chapter2.pk, self.section2.pk)

    def test_section_create_page(self):
        """
        Create section page loads
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.section_create(request, self.campaign.pk, self.chapter.pk)

        # check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_section_create(self):
        """
        Create section
        """

        form_data = {'title': 'test section title', 'content': 'yyyyyyyyyy', 'order': '1'}
        form = forms.SectionForm(data=form_data)
        new_section = form.save(commit=False)
        new_section.user = self.user
        new_section.campaign = self.campaign
        new_section.chapter = self.chapter
        new_section.save()

        new_section = models.Section.objects.get(pk=new_section.pk)
        sections = models.Section.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_section, sections)

    def test_section_edit_page(self):
        """
        Edit section page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.section_update(request, self.campaign.pk, self.chapter.pk, self.section.pk)

        # make sure the section information is on the page
        self.assertContains(response, self.campaign.title, status_code=200)
        self.assertContains(response, self.chapter.title, status_code=200)
        self.assertContains(response, self.section.title, status_code=200)
        self.assertContains(response, self.section.content, status_code=200)
        self.assertContains(response, self.section.order, status_code=200)

    def test_section_edit(self):
        """
        Edit section
        """

        form_data = {'title': 'test section title EDIT', 'content': 'yyyyyyyyyy EDIT', 'order': '2'}
        form = forms.SectionForm(data=form_data)
        new_section = form.save(commit=False)
        new_section.user = self.user
        new_section.campaign = self.campaign
        new_section.chapter = self.chapter
        new_section.save()

        new_section = models.Section.objects.get(title="test section title EDIT")
        sections = models.Section.objects.all()

        self.assertTrue(form.is_valid())
        self.assertIn(new_section, sections)

    def test_section_delete_page(self):
        """
        Delete section page contains the correct information
        """

        # create an instance of a GET request
        request = self.factory.get('home')

        # simulate a logged-in user
        request.user = self.user

        # test the view
        response = views.section_delete(request, self.campaign.pk, self.chapter.pk, self.section.pk)

        # make sure the section information is on the page
        self.assertContains(response, self.section.title, status_code=200)

    def test_section_delete(self):
        """
        Delete section
        """

        form_data = {'title': 'test section title'}
        form = forms.DeleteSectionForm(data=form_data)
        new_section = form.save(commit=False)
        new_section.user = self.user
        new_section.campaign = self.campaign
        new_section.chapter = self.chapter
        new_section.save()

        self.assertTrue(form.is_valid())
