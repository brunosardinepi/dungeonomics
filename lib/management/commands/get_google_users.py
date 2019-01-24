from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialAccount


class Command(BaseCommand):
    help = "Finds all Google accounts that haven't updated their password"

    def get_users(self, provider):
        social_accounts = SocialAccount.objects.filter(provider=provider)
        users = []
        for social_account in social_accounts:
            users.append(User.objects.get(pk=social_account.user_id))
        return users

    def handle(self, *args, **options):
        users = self.get_users("google")

        count = 0
        for user in users:
            if not user.has_usable_password():
                count+=1

        print("final count = {}".format(count))
