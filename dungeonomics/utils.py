from django.conf import settings
from django.db.models import Avg

from tavern.models import Review
from characters.models import Monster, NPC, Player
from items.models import Item
from locations.models import Location, World
from tables.models import Table


def image_is_valid(request, form):
    if form.is_valid():
        image_raw = form.cleaned_data.get('image', False)
        if image_raw:
            if 'ImageFieldFile' in str(type(image_raw)):
                return True
            else:
                image_type = image_raw.content_type.split('/')[0]
                if image_type in settings.UPLOAD_TYPES:
                    if image_raw._size <= settings.MAX_IMAGE_UPLOAD_SIZE:
                        return True
                    else:
                        return "bad size"
                else:
                    return "bad type"

def at_tagging(request):
    monsters_raw = Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = Player.objects.filter(user=request.user).order_by('character_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.character_name
    worlds_raw = World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    tables_raw = Table.objects.filter(user=request.user).order_by('name')
    tables = {}
    for table in tables_raw:
        tables[table.pk] = table.name

    return {
        'monsters': monsters,
        'npcs': npcs,
        'items': items,
        'players': players,
        'worlds': worlds,
        'locations': locations,
        'tables': tables,
    }

def rating_monster(monster):
    # find the average rating
    return Review.objects.filter(
        monster=monster).aggregate(
        Avg('score'))['score__avg'] or 0.00

def rating_npc(npc):
    # find the average rating
    return Review.objects.filter(
        npc=npc).aggregate(
        Avg('score'))['score__avg'] or 0.00

def rating_player(player):
    # find the average rating
    return Review.objects.filter(
        player=player).aggregate(
        Avg('score'))['score__avg'] or 0.00
