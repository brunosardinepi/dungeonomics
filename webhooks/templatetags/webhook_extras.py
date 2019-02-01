import json

from django import template

from webhooks.models import Webhook, WebhookAttribute


register = template.Library()

@register.simple_tag
def get_webhook_attribute(webhook, key):
    try:
        attribute = WebhookAttribute.objects.get(webhook=webhook, key=key)
    except WebhookAttribute.DoesNotExist:
        attribute = None

    return attribute

@register.simple_tag
def get_webhook_sns_message(webhook):
    try:
        attribute = WebhookAttribute.objects.get(webhook=webhook, key="Message")
    except WebhookAttribute.DoesNotExist:
        attribute = None

    if attribute:
        try:
            attribute = json.loads(attribute.value)
        except:
            attribute = None

    return attribute
