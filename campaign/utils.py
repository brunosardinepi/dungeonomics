from bs4 import BeautifulSoup

from django.shortcuts import get_object_or_404

from campaign.models import Campaign
from characters.models import Monster, NPC, Player
from items.models import Item
from locations.models import Location, World
from tables.models import Table


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

def get_content_url(link):
    str_link = str(link)

    url = link.get('href')

    if "dungeonomics.com/" in str_link:
        url = url.split(".com/")[1]
    elif "dungeonomics.com:8000" in str_link:
        url = url.split(".com:8000/")[1]
    elif "../" in str_link:
        done = False
        while done == False:
            try:
                url = url.split("../", 1)[1]
            except IndexError:
                done = True

    return url

def get_url_object(url):
    resource = url.split("/")[0]

    if resource == "characters":
        character_type = url.split("characters/")[1]
        character_pk = character_type.split("/", 1)[1]
        character_pk = character_pk.replace("/", "")
        character_type = character_type.split("/", 1)[0]

        if character_type == "monster":
            try:
                obj = Monster.objects.get(pk=character_pk)
            # could be a character that doesn't exist anymore but
            # the link never got updated
            except Monster.DoesNotExist:
                obj = None
        elif character_type == "npc":
            try:
                obj = NPC.objects.get(pk=character_pk)
            except NPC.DoesNotExist:
                obj = None
        # don't think i want to bring these in
        elif character_type == "player":
            obj = None

    elif resource == "items":
        item_pk = url.split("items/")[1]
        item_pk = item_pk.replace("/", "")

        try:
            obj = Item.objects.get(pk=item_pk)
        except Item.DoesNotExist:
            obj = None

    elif resource == "tables":
        table_pk = url.split("tables/")[1]
        table_pk = table_pk.replace("/", "")

        try:
            obj = Table.objects.get(pk=table_pk)
        except Table.DoesNotExist:
            obj = None

    elif resource == "locations":
        location_type = url.split("locations/")[1]
        location_pk = location_type.split("/", 1)[1]
        location_pk = location_pk.replace("/", "")
        location_type = location_type.split("/", 1)[0]

        if location_type == "world":
            try:
                obj = World.objects.get(pk=location_pk)
            except World.DoesNotExist:
                obj = None
        elif location_type == "location":
            try:
                obj = Location.objects.get(pk=location_pk)
            except Location.DoesNotExist:
                obj = None
    else:
        # may not be a dungeonomics url
        obj = None

    return obj

def replace_content_urls(item, asset_references):
    # find all the assets in the content
    # for each asset, find the object type and its pk
    # find that object in the asset_references section, looking at old_pk
    # swap the old_pk for the new_pk

    soup = BeautifulSoup(item.content, 'html.parser')

    for link in soup.find_all('a'):
        url = get_content_url(link)

        obj = get_url_object(url)

        if obj:
            obj_old_pk = obj.pk
        else:
            continue

        if isinstance(obj, Monster):
            new_pk = asset_references['monsters'][obj_old_pk]
        elif isinstance(obj, NPC):
            new_pk = asset_references['npcs'][obj_old_pk]
        elif isinstance(obj, Item):
            new_pk = asset_references['items'][obj_old_pk]
        elif isinstance(obj, World):
            new_pk = asset_references['worlds'][obj_old_pk]
        elif isinstance(obj, Location):
            new_pk = asset_references['locations'][obj_old_pk]
        elif isinstance(obj, Table):
            new_pk = asset_references['tables'][obj_old_pk]

        new_url = url.replace(str(obj_old_pk), str(new_pk))

        item.content = item.content.replace(url, new_url)
        item.save()
