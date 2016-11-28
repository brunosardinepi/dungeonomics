# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.utils import timezone

# from . import models


# class CampaignModelTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username="testuser", password="testpassword")

#     def test_campaign_creation(self):
#         campaign = models.Campaign.objects.create(
#             user=self.user,
#             title="Campaign Title",
#             description="This is the campaign description."
#         )
#         now = timezone.now()
#         self.assertLess(campaign.created_at, now)