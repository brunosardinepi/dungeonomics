from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialAccount


class Command(BaseCommand):
    help = "Finds all Google accounts and emails them"

    def get_users(self, provider):
        social_accounts = SocialAccount.objects.filter(provider=provider)
        users = []
        for social_account in social_accounts:
            users.append(User.objects.get(pk=social_account.user_id))
        return users

    def handle(self, *args, **options):
        users = self.get_users("google")

        subject = "Dungeonomics Google authentication will be removed February 1"
        text_body = "Our update to remove Google authentication will go live next Friday (February 1) at noon CST. We've identified you as one of the users who has not updated your Dungeonomics password. Please make sure you have reset your Dungeonomics password (https://dungeonomics.com/accounts/password/reset/) so you can still login after Google authentication has been removed. You can email us at dungeonomics@gmail.com if you need help and we'll make sure you're all set. To make sure we aren't spamming you, this will be the only reminder via email."
        html_body = "Our update to remove Google authentication will go live next Friday (February 1) at noon CST. We've identified you as one of the users who has not updated your Dungeonomics password. Please make sure you have reset your Dungeonomics password (<a href='https://dungeonomics.com/accounts/password/reset/'>https://dungeonomics.com/accounts/password/reset/</a>) so you can still login after Google authentication has been removed. You can email us at dungeonomics@gmail.com if you need help and we'll make sure you're all set. To make sure we aren't spamming you, this will be the only reminder via email."

        count = 0
        for user in users:
            if not user.has_usable_password():
                message = EmailMultiAlternatives(subject, text_body, to=[user.email])
                message.attach_alternative(html_body, "text/html")
                message.send()
                print("email sent to {}".format(user.email))

                count+=1

        print("final count = {}".format(count))
