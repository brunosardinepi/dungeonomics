from django.shortcuts import get_object_or_404

from campaign.models import Campaign
from characters.models import Player


def has_campaign_access(user, campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    if user == campaign.user:
        return True

    campaign_players = campaign.player_set.all()
    players = Player.objects.filter(user=user)
    for player in players:
        if player in campaign_players:
            return True

    return False