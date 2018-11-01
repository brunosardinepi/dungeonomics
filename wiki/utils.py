from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from dungeonomics import config


def is_wiki_admin(user):
    if user.email in config.settings['wiki_admins']:
        return True
    return False


def is_article_admin(user, article):
    if user in article.admins.all():
        return True
    return False

def add_article_admins(article):
    for email in config.settings['wiki_admins']:
        try:
            user = User.objects.get(email=email)
            article.admins.add(user)
        except User.DoesNotExist:
            pass
