from django import template

from campaign.models import Campaign


register = template.Library() 

@register.inclusion_tag('campaign_nav.html')
def nav_campaign_list(request): 
    '''Returns dictionary of campaigns to display in navigation pane'''
    user = None
    if request.user.is_authenticated():
        user = request.user.pk

    campaigns = Campaign.objects.filter(
        user=user
    ).order_by(
        'title'
    ).values(
        'id', 'title'
    )
    return {'campaigns': campaigns}