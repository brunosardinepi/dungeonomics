from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

import unittest
from model_mommy import mommy

from . import models
from campaign.models import Campaign
from characters.models import Player


class PostTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=3)

        self.campaigns = mommy.make(
            Campaign,
            user=self.users[0],
            _quantity=2,
            _fill_optional=True,
        )
        self.campaigns[1].user = self.users[1]
        self.campaigns[1].save()

        self.players = mommy.make(
            Player,
            user=self.users[1],
            _quantity=3,
            _fill_optional=True,
        )
        self.players[1].campaigns.add(self.campaigns[0])
        self.players[2].campaigns.add(self.campaigns[0])

        self.post = mommy.make(
            models.Post,
            user=self.users[0],
            campaign=self.campaigns[0],
            _fill_optional=True,
        )

        self.comments = mommy.make(
            models.Comment,
            user=self.users[0],
            post=self.post,
            _quantity=2,
            _fill_optional=True,
        )

    def test_post_creation_time(self):
        post = models.Post.objects.create(
            user=self.users[0],
            title="test post time",
            body="ajksdhflasdjkfhalsdkjfhalsdkjfhasdf",
            campaign=self.campaigns[0],
        )
        now = timezone.now()
        self.assertLess(post.date, now)

    def test_comment_creation_time(self):
        comment = models.Comment.objects.create(
            user=self.users[0],
            body="testingtime",
            post=self.post,
        )
        now = timezone.now()
        self.assertLess(comment.date, now)

    def test_post_exists(self):
        posts = models.Post.objects.all()

        self.assertIn(self.post, posts)

    def test_comment_exists(self):
        comments = models.Comment.objects.all()

        self.assertIn(self.comments[0], comments)
        self.assertIn(self.comments[1], comments)

    def test_post_create_page_auth_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)

    def test_post_create_page_auth_player(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 200)

    def test_post_create_page_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk))

        self.assertEqual(response.status_code, 404)

    def test_post_create_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk))

        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk), 302, 200)

    def test_post_create_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk), {
            'title': "this is my title",
            'body': "check out this body",
        })
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaigns[0].pk), 302, 200)

        response = self.client.get('/campaign/{}/party/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is my title")
        self.assertContains(response, "check out this body")

    def test_post_create_auth_perms(self):
        self.client.force_login(self.users[1])
        response = self.client.post('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk), {
            'title': "this is my title",
            'body': "check out this body",
        })
        self.assertRedirects(response, '/campaign/{}/party/'.format(self.campaigns[0].pk), 302, 200)

        response = self.client.get('/campaign/{}/party/'.format(self.campaigns[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "this is my title")
        self.assertContains(response, "check out this body")

    def test_post_create_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.post('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk), {
            'title': "this is my title",
            'body': "check out this body",
        })
        self.assertEqual(response.status_code, 404)

    def test_post_create_no_auth(self):
        response = self.client.post('/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk), {
            'title': "this is my title",
            'body': "check out this body",
        })
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/create/'.format(self.campaigns[0].pk, self.post.pk), 302, 200)

    def test_post_page_auth_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertContains(response, "post-delete")
        self.assertContains(response, self.comments[0].body)
        self.assertContains(response, self.comments[1].body)

    def test_post_page_auth_player(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertNotContains(response, "post-delete")
        self.assertContains(response, self.comments[0].body)
        self.assertContains(response, self.comments[1].body)

    def test_post_page_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))

        self.assertEqual(response.status_code, 404)

    def test_post_page_no_auth(self):
        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))

        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), 302, 200)

    def test_comment_create_owner(self):
        self.client.force_login(self.users[0])
        response = self.client.post('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), {
            'body': "check out this body",
        })
        self.assertRedirects(response, '/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), 302, 200)

        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "check out this body")

    def test_comment_create_auth_perms(self):
        self.client.force_login(self.users[1])
        response = self.client.post('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), {
            'body': "check out this body",
        })
        self.assertRedirects(response, '/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), 302, 200)

        response = self.client.get('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "check out this body")

    def test_comment_create_auth_no_perms(self):
        self.client.force_login(self.users[2])
        response = self.client.post('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), {
            'body': "check out this body",
        })
        self.assertEqual(response.status_code, 404)

    def test_comment_create_no_auth(self):
        response = self.client.post('/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), {
            'body': "check out this body",
        })
        self.assertRedirects(response, '/accounts/login/?next=/campaign/{}/party/posts/{}/'.format(self.campaigns[0].pk, self.post.pk), 302, 200)