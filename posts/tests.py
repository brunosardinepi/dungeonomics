from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from . import models
from campaign.models import Campaign
from characters.models import Player


class PostTest(TestCase):
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

        self.user3 = User.objects.create_user(
            username='testuser3',
            email='test3@test.test',
            password='testpassword',
        )

        self.campaign = Campaign.objects.create(
            user=self.user,
            title="test campaign",
        )

        self.campaign2 = Campaign.objects.create(
            user=self.user2,
            title="test campaign 2",
        )

        self.player = Player.objects.create(
            user=self.user2,
            player_name="user no 2",
            character_name="Bullwinkle",
        )

        self.player2 = Player.objects.create(
            user=self.user2,
            player_name="Charlie",
            character_name="Vomit",
        )
        self.player2.campaigns.add(self.campaign)

        self.player3 = Player.objects.create(
            user=self.user2,
            player_name="Ripley",
            character_name="Indoor dog",
        )
        self.player3.campaigns.add(self.campaign)

        self.post = models.Post.objects.create(
            user=self.user,
            title="testpost1",
            body="ppppwppwpwpwpwpw",
            campaign=self.campaign,
        )

    def test_post_creation_time(self):
        post = models.Post.objects.create(
            user=self.user,
            title="test post time",
            body="ajksdhflasdjkfhalsdkjfhalsdkjfhasdf",
            campaign=self.campaign,
        )
        now = timezone.now()
        self.assertLess(post.date, now)

    def test_post_exists(self):
        posts = models.Post.objects.all()

        self.assertIn(self.post, posts)

    def test_post_create_page_auth_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)

    def test_post_create_page_auth_player(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 200)

    def test_post_create_page_auth_no_perms(self):
        self.client.login(username='testuser3', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaign.pk))

        self.assertEqual(response.status_code, 404)

    def test_post_create_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaign.pk))

        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/create/'.format(self.campaign.pk), 302, 200)

    def test_post_create(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/campaign/{}/party/posts/create/'.format(self.campaign.pk), {
            'title': "this is my title",
            'body': "check out this body",
        })
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaign.pk), 302, 200)

        response = self.client.get('/campaign/{}/party/'.format(self.campaign.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is my title")
        self.assertContains(response, "check out this body")

    def test_post_page_auth_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaign.pk, self.post.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertContains(response, "post-delete")

    def test_post_page_auth_player(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaign.pk, self.post.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertNotContains(response, "post-delete")

    def test_post_page_auth_no_perms(self):
        self.client.login(username='testuser3', password='testpassword')
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaign.pk, self.post.pk))

        self.assertEqual(response.status_code, 404)

    def test_post_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaign.pk, self.post.pk))

        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/{}/'.format(self.campaign.pk, self.post.pk), 302, 200)