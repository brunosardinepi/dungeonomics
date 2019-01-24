import json
import unittest

from django.contrib.auth.models import User
from django.test import Client, TestCase

from model_mommy import mommy

from .models import Webhook, WebhookAttribute
from . import views


class ItemTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)
        self.users[0].email = 'gn9012@gmail.com'
        self.users[0].save()

        self.webhooks = mommy.make(
            Webhook,
            _quantity=4,
            _fill_optional=True,
        )
        self.webhooks[2].user = self.users[1]
        self.webhooks[3].user = self.users[1]
        self.webhooks[2].save()
        self.webhooks[3].save()

        self.webhookattributes = mommy.make(
            WebhookAttribute,
            webhook=self.webhooks[0],
            _quantity=10,
            _fill_optional=True,
        )
        self.webhookattributes[2].webhook = self.webhooks[1]
        self.webhookattributes[3].webhook = self.webhooks[1]
        self.webhookattributes[4].webhook = self.webhooks[1]
        self.webhookattributes[5].webhook = self.webhooks[2]
        self.webhookattributes[6].webhook = self.webhooks[2]
        self.webhookattributes[7].webhook = self.webhooks[3]
        self.webhookattributes[8].webhook = self.webhooks[3]
        self.webhookattributes[9].webhook = self.webhooks[3]
        for attribute in self.webhookattributes:
            attribute.save()

    def test_webhook_exists(self):
        webhooks = Webhook.objects.all()
        for webhook in self.webhooks:
            self.assertIn(webhook, webhooks)

    def test_webhookattribute_exists(self):
        webhookattributes = WebhookAttribute.objects.all()
        for attribute in self.webhookattributes:
            self.assertIn(attribute, webhookattributes)

    def test_webhook_list(self):
        response = self.client.get('/webhooks/')
        self.assertRedirects(response, '/accounts/login/?next=/webhooks/', 302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/webhooks/')
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.users[0])
        response = self.client.get('/webhooks/')
        self.assertEqual(response.status_code, 200)
        for webhook in self.webhooks:
            self.assertContains(response, "{}:{}".format(webhook.provider, webhook.pk))

    def test_webhook_detail(self):
        response = self.client.get('/webhooks/{}/'.format(self.webhooks[0].pk))
        self.assertRedirects(response,
            '/accounts/login/?next=/webhooks/{}/'.format(self.webhooks[0].pk),
            302, 200)

        self.client.force_login(self.users[1])
        response = self.client.get('/webhooks/{}/'.format(self.webhooks[0].pk))
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.users[0])
        response = self.client.get('/webhooks/{}/'.format(self.webhooks[0].pk))
        self.assertEqual(response.status_code, 200)

    def test_webhook_sns(self):
        response = self.client.post('/webhooks/sns/',
            json.dumps({'key': 'value'}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
