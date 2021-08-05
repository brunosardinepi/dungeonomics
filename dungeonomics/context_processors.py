from campaign.models import Campaign
from characters.models import Player, Monster, NPC
from django.urls import reverse
from items.models import Item
from locations.models import World, Location
from tables.models import Table


def navbar(request):
    if request.user.is_authenticated:
        return {
            'sections': [
                {
                    'name': 'Home',
                    'type': 'single',
                    'links': [
                        {
                            'name': 'Home',
                            'url': reverse('home'),
                        },
                    ],
                    'queryset': '',
                    'icon': 'fa-home',
                },
                {
                    'name': 'Campaigns',
                    'type': 'dropdown',
                    'links': [
                        {
                            'name': 'Create campaign',
                            'url': reverse('campaign:campaign_create'),
                        },
                        {
                            'name': 'Import campaign',
                            'url': reverse('campaign:campaign_import'),
                        },
                    ],
                    'queryset': Campaign.objects.filter(user=request.user),
                    'icon': 'fa-dice-d20',
                },
                {
                    'name': 'Players',
                    'type': 'dropdown',
                    'links': [],
                    'queryset': Player.objects.filter(user=request.user),
                    'icon': 'fa-user-astronaut',
                },
                {
                    'name': 'Monsters',
                    'type': 'dropdown',
                    'links': [],
                    'queryset': Monster.objects.filter(user=request.user),
                    'icon': 'fa-dragon',
                },
                {
                    'name': 'NPCs',
                    'type': 'dropdown',
                    'links': [],
                    'queryset': NPC.objects.filter(user=request.user),
                    'icon': 'fa-address-card',
                },
                {
                    'name': 'Items',
                    'type': 'dropdown',
                    'links': [
                        {
                            'name': 'Create item or spell',
                            'url': reverse('items:item_create'),
                        },
                    ],
                    'queryset': Item.objects.filter(user=request.user),
                    'icon': 'fa-axe-battle',
                },
                {
                    'name': 'Locations',
                    'type': 'dropdown',
                    'links': [
                        {
                            'name': 'Create world',
                            'url': reverse('locations:world_create'),
                        },
                    ],
                    'queryset': World.objects.filter(user=request.user),
                    'icon': 'fa-map-marked-alt',
                },
                {
                    'name': 'Tables',
                    'type': 'dropdown',
                    'links': [
                        {
                            'name': 'Create table',
                            'url': reverse('tables:table_create'),
                        },
                    ],
                    'queryset': Table.objects.filter(user=request.user),
                    'icon': 'fa-table',
                },
                {
                    'name': 'Tavern',
                    'type': 'single',
                    'links': [
                        {
                            'name': 'Tavern',
                            'url': reverse('tavern:tavern'),
                        },
                    ],
                    'queryset': '',
                    'icon': 'fa-beer',
                },
                {
                    'name': 'Wiki',
                    'type': 'single',
                    'links': [
                        {
                            'name': 'Wiki',
                            'url': reverse('wiki:article_detail'),
                        },
                    ],
                    'queryset': '',
                    'icon': 'fa-book',
                },
                {
                    'name': 'Account',
                    'type': 'dropdown',
                    'links': [
                        {
                            'name': request.user.email,
                            'url': reverse('profile'),
                        },
                        {
                            'name': 'Donate',
                            'url': reverse('donate'),
                        },
                        {
                            'name': 'Logout',
                            'url': reverse('account_logout'),
                        },
                    ],
                    'queryset': '',
                    'icon': 'fa-cogs',
                },
            ]
        }
    return {}
