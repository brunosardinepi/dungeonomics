from itertools import chain

from django import template
from django.shortcuts import get_object_or_404

from campaign.models import Campaign
from characters.models import Monster, NPC, Player


register = template.Library()

@register.simple_tag
def nav_campaign_list(request):
    # get the user is logged in, None if not
    user = None
    if request.user.is_authenticated:
        user = request.user.pk

    # get the Campaigns that the user owns
    campaigns = Campaign.objects.filter(user=user)

    # get the user's Players
    players = Player.objects.filter(user=user)

    # find the Campaigns that each Player is a member of
    # and put them in the parties list
    parties = []
    for player in players:
        party = player.campaigns.all()
        for p in party:
            parties.append(p)

    # merge the campaigns and parties querysets
    campaigns = list(chain(campaigns, parties))
    # remove duplicates
    campaigns = list(set(campaigns))
    # sort by campaign.title
    campaigns = sorted(campaigns, key=lambda s: s.title.lower())
    return campaigns

@register.filter
def model_name(obj):
    return obj.__class__.__name__.lower()

@register.simple_tag
def is_campaign_owner(user, campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    # return True if the user is the Campaign owner
    return user == campaign.user

@register.simple_tag
def campaign_has_players(campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    # return True if the Campaign has any Players
    return campaign.player_set.all().count() > 0

@register.filter
def post_user(email):
    return email.split('@')[0]

@register.filter
def asset_title(obj):
    if obj == "npc":
        return obj.upper()
    else:
        return obj.capitalize()
