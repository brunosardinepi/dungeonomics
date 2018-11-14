from itertools import chain

from django.conf import settings
from django.core import serializers
from django.db.models import Avg

from tavern.models import Review
from characters.models import GeneralCharacter
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
    characters = GeneralCharacter.objects.filter(user=request.user).order_by('name')
    items = Item.objects.filter(user=request.user).order_by('name')
    worlds = World.objects.filter(user=request.user).order_by('name')
    locations = Location.objects.filter(user=request.user).order_by('name')
    tables = Table.objects.filter(user=request.user).order_by('name')

    combined_assets = list(chain(characters, items, worlds, locations, tables))

    assets = []
    for asset in combined_assets:
        assets.append({
            'name': asset.name,
            'url': asset.get_full_url(),
        })

    return assets

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
