import smtplib

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialAccount

from dungeonomics import settings


class Command(BaseCommand):
    help = "Finds all Facebook accounts"

    def email_user(self, user):
        subject = "Dungeonomics Facebook authentication wil be removed this Friday"
        body = "Our update to remove Facebook authentication will go live this Friday 12/28 at noon. We've identified you as one of the users who has not updated your Dungeonomics password. Please make sure you have reset your Dungeonomics password (https://dungeonomics.com/accounts/password/reset/) so you can still login after Facebook authentication has been removed. You can reply to this email if you need help and we'll make sure you're all set."
        content = "\r\n".join([
            "From: {}".format(settings.DEFAULT_FROM_EMAIL),
            "To: {}".format(user.email),
            "Subject: {}".format(subject),
            "",
            body,
        ])

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.ehlo()
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            server.sendmail(settings.DEFAULT_FROM_EMAIL, user.email, content)
            server.close()
        except Exception as e:
            print("couldn't connect")
            print(e)

    def get_users(self, provider):
        social_accounts = SocialAccount.objects.filter(provider=provider)
        users = []
        for social_account in social_accounts:
            users.append(User.objects.get(pk=social_account.user_id))
        return users

    def handle(self, *args, **options):
        users = self.get_users("facebook")
        print(len(users))
        for user in users:
            u = User.objects.get(pk=user.pk)
            email_sent = ['mgonza39@jhu.edu','thursbymartin@gmail.com','sharptoothfox@gmail.com','habermanjc@gmail.com','garyrolen@aol.com','ianufyrebird@gmail.com','devolutionary@devolutionary.net','onid16@gmail.com','jayhull@gmail.com','gibzy94@hotmail.co.uk','m0wd3r@gmail.com','mk.harris8@gmail.com','pnmillen@gmail.com','michaells95@live.com','fjankowski97@gmail.com','kjshunk@comcast.net','dabbott60115@yahoo.com','mordaken@yahoo.com','handley134@gmail.com','will.hoene@gmail.com','zenthazar@yahoo.com','yahkub@gmail.com','mcvoid@mcvoid.org','honey.latte@yahoo.com','zeratul257@yahoo.com','aidanrobbins@mac.com','kryptkat@hotmail.com','jjosephbarron@gmail.com','martinmj1989@aol.com','mharris161@gmail.com','hoggeta@gmail.com','tylertheintern@gmail.com','da.fiery.winged.dragon@gmail.com','aaron_asbury@live.com','fearlesshornet@gmail.com','gilnean21@yahoo.com','graciious@rogers.com','bradmarston@hotmail.com','ruamokutakaroa@gmail.com','crazyshepard@gmail.com','johnlemas@gmail.com','chdwck37@gmail.com','embracethesack@yahoo.com','mbtz@outlook.com','candreschefski@shaw.ca','pimpdaddypat79@hotmail.com','harrisonbarth@yahoo.com','rtackabu@umflint.edu','flowandebb@live.com','zacharyfdeane@gmail.com','crackalackster6@yahoo.com','jvanzile10@gmail.com','jzarrow@gmail.com','legrand@nsuok.edu','andrewstubing@yahoo.com','patonjf@hotmail.com','jayson1717@aol.com','robertcoxvideo@gmail.com','jarrod.maistros@gmail.com','ccjacobs24@gmail.com','halliwell.tyler@gmail.com','feuergeist@gmail.com','frozenachos@gmail.com','awesomesomething@gmail.com','benbrommell@gmail.com','plamenkovatchev007@gmail.com','vitaly-gann@live.com','chrizzern@gmail.com','forresthol@gmail.com','jacobyestrepsky@hotmail.com','amazingsleep@gmail.com','plundyman@gmail.com','mcknickknock@gmail.com','tobal_be@live.cl','zackava99@gmail.com','jrseiwert@hotmail.com','dargie1@live.com','vegeta84_00@yahoo.com','ajoyce86@gmail.com','cordle.matthew@gmail.com','squires_11teen@hotmail.com','anubhavbala@yahoo.com','motasmail@gmail.com']
            if not u.email in email_sent:
                if not u.has_usable_password():
#                    self.email_user(user)