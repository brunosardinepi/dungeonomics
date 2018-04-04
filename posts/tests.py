from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest

from . import models
from campaign.models import Campaign


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