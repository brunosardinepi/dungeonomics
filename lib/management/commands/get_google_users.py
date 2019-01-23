from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialAccount


class Command(BaseCommand):
    help = "Finds all Google accounts"

    # select count(*) from socialaccount_socialaccount where provider = 'google';
    def get_users(self, provider):
        social_accounts = SocialAccount.objects.filter(provider=provider)
        users = []
        for social_account in social_accounts:
            users.append(User.objects.get(pk=social_account.user_id))
        return users

    def handle(self, *args, **options):
        users = self.get_users("google")
        print(len(users))
        count = 0
        for user in users:
            u = User.objects.get(pk=user.pk)
            if not u.has_usable_password():
                count+=1
        print(count)