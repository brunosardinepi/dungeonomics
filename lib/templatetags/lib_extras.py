from django import template
from django.shortcuts import get_object_or_404

from campaign.models import Campaign


register = template.Library()

@register.inclusion_tag('campaign_nav.html')
def nav_campaign_list(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk

    campaigns = Campaign.objects.filter(user=user).order_by('title').values('id', 'title')
    return {'campaigns': campaigns}

@register.filter
def model_name(obj):
    return obj.__class__.__name__.lower()

@register.simple_tag
def has_players(campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    # return True if the Campaign has any Players
    return campaign.player_set.all().count() > 0