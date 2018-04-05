from django.conf import settings

from characters.models import Monster, NPC, Player
from items.models import Item
from locations.models import Location, World


def image_is_valid(request, form):
    if form.is_valid():
        image_raw = form.cleaned_data.get('image', False)
        if image_raw:
#            if type(image_raw) == 'django.core.files.uploadedfile.InMemoryUploadedFile':
#                image_type = image_raw.content_type.split('/')[0]
#                if image_type in settings.UPLOAD_TYPES:
#                    if image_raw._size <= settings.MAX_IMAGE_UPLOAD_SIZE:
#                        return True
#                    else:
#                        return "bad size"
#                else:
#                    return "bad type"

            try:
                image_type = image_raw.content_type.split('/')[0]
            except:
                image_type = 'none'
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

    return {
        'monsters': monsters,
        'npcs': npcs,
        'items': items,
        'players': players,
        'worlds': worlds,
        'locations': locations,
    }