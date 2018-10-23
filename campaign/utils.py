from bs4 import BeautifulSoup
from itertools import chain
import json
from shutil import copyfile

from django.core import serializers
from django.shortcuts import get_object_or_404

from campaign.models import Campaign, Chapter, Section
from characters.models import Monster, NPC, Player
from dungeonomics import settings
from items.models import Item
from locations.models import Location, World, create_random_string
from tables.models import Table, TableOption


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

def rating_stars_html(rating):
    # round to nearest 0.5
    rating = round(rating * 2) / 2

    # html template for an empty star
    empty_star = '<i class="far fa-star"></i>'

    # html template for a half star
    half_star = '<i class="fas fa-star-half-alt"></i>'

    # html template for a full star
    full_star = '<i class="fas fa-star"></i>'

    if rating == 0:
        html = empty_star * 5
    elif rating % 1 == 0:
        html = (full_star * int(rating)) + (empty_star * int(5 - rating))
    elif rating % 1 == 0.5:
        html = (full_star * int(rating - 0.5)) + half_star + (empty_star * int(5 - rating - 0.5))

    return html


def campaign_export(campaign):
    chapters_queryset = Chapter.objects.filter(campaign=campaign).order_by('order')
    sections_queryset = Section.objects.filter(campaign=campaign).order_by('order')
    combined_list = list(chain(chapters_queryset, sections_queryset))

    # go through each chapter and section
    # find all of the hyperlinks
    # look through the dungeonomics links
    # get the type (item, monster, npc, player)
    # pull a copy of that resource and add it to a list
    # at the end, combine the list with the campaign items list
    # then serialize it

    additional_assets = []
    added_other = []
    added_worlds = []
    added_locations = []
    added_tables = []

    for item in combined_list:

        soup = BeautifulSoup(item.content, 'html.parser')

        for link in soup.find_all('a'):
            url = get_content_url(link)

            obj = get_url_object(url)

            if obj:

                # if World, get all the child locations
                # if Location, get the World and all child locations
                if isinstance(obj, World):
                    if obj.pk not in added_worlds:
                        # get all of the Locations that belong to this World
                        locations = Location.objects.filter(world=obj)

                        # add all of the new locations to lists for tracking
                        for location in locations:
                            additional_assets.append(location)
                            added_locations.append(location.pk)

                        # add the World to a list for tracking
                        additional_assets.append(obj)
                        added_worlds.append(obj.pk)

                elif isinstance(obj, Location):
                    if obj.pk not in added_locations:
                        # add the location to our list
                        additional_assets.append(obj)
                        added_locations.append(obj.pk)

                        # get this Location's World
                        world = World.objects.get(pk=obj.world.pk)

                        if world.pk not in added_worlds:
                            # append it to our list
                            additional_assets.append(world)

                            # get the World's Locations, excluding the Location we already have
                            locations = Location.objects.filter(world=world).exclude(pk=obj.pk)

                            # add all of the new locations to the list
                            for location in locations:
                                additional_assets.append(location)
                                added_locations.append(location.pk)

                elif isinstance(obj, Table):
                    if obj.pk not in added_tables:
                        # get all of the Table Options that belong to this Table
                        table_options = TableOption.objects.filter(table=obj)

                        # add all of the new Table Options to a list for tracking
                        for table_option in table_options:
                            additional_assets.append(table_option)

                        # add the Table to a list for tracking
                        additional_assets.append(obj)
                        added_tables.append(obj.pk)

                else:
                    if obj.pk not in added_other:
                        additional_assets.append(obj)
                        added_other.append(obj.pk)

    combined_list = list(chain(combined_list, additional_assets))
    campaign_items = serializers.serialize("json", combined_list, indent=2)

    return campaign_items


def campaign_import(user, campaign, json_export):
    chapters, sections, others = ([] for i in range(3))
    model_types = [
        "Monster",
        "NPC",
        "Item",
        "World",
        "Location",
        "Table",
        "TableOption",
    ]

    for obj in serializers.deserialize("json", json_export):
        if isinstance(obj.object, Chapter):
            chapters.append(obj.object)
        elif isinstance(obj.object, Section):
            sections.append(obj.object)
        elif obj.object.__class__.__name__ in model_types:
            others.append(obj.object)

    asset_references = {
        "monsters": {},
        "npcs": {},
        "items": {},
        "worlds": {},
        "locations": {},
        "tables": {},
        "tableoptions": {},
    }

    # for each "other" asset,
    # create a copy of the asset
    # and update a dictionary that holds a reference of the old pk and the new pk

    for other in others:
        # grab the old pk for reference
        old_pk = other.pk

        # create a copy of the asset
        other.pk = None
        other.user = user

        if isinstance(other, World) or isinstance(other, Location):
            if other.image:

                # create a new filename
                random_string = create_random_string()
                ext = other.image.url.split('.')[-1]
                new_filename = "media/user/images/%s.%s" % (random_string, ext)

                # copy the old file to a new file
                # and save it to the new object
                old_image_url = settings.MEDIA_ROOT + other.image.name
                new_image_url = settings.MEDIA_ROOT + new_filename
                copyfile(old_image_url, new_image_url)
                other.image = new_filename

        other.save()

        new_pk = other.pk

        if isinstance(other, Monster):
            asset_references['monsters'][old_pk] = new_pk
        elif isinstance(other, NPC):
            asset_references['npcs'][old_pk] = new_pk
        elif isinstance(other, Item):
            asset_references['items'][old_pk] = new_pk
        elif isinstance(other, World):
            asset_references['worlds'][old_pk] = new_pk
        elif isinstance(other, Location):
            asset_references['locations'][old_pk] = new_pk
        elif isinstance(other, Table):
            asset_references['tables'][old_pk] = new_pk
        elif isinstance(other, TableOption):
            asset_references['tableoptions'][old_pk] = new_pk

    # update any content with new pks
    # must be done after asset_references is populated
    for other in others:
        # everything has 'content' except TableOption
        if not isinstance(other, TableOption):
            replace_content_urls(other, asset_references)

    for old_pk, new_pk in asset_references['tableoptions'].items():
        # for each tableoption, set the table to the newly created table
        old_tableoption = TableOption.objects.get(pk=old_pk)
        new_tableoption = TableOption.objects.get(pk=new_pk)
        old_table = old_tableoption.table
        new_table = Table.objects.get(pk=asset_references['tables'][old_table.pk])
        new_tableoption.table = new_table
        new_tableoption.save()

    for old_pk, new_pk in asset_references['locations'].items():
        # for each location, set the parent location to the new parent location.
        # also, set the world to the new world
        old_location = Location.objects.get(pk=old_pk)
        if old_location.parent_location:
            old_location_parent = old_location.parent_location

        new_location = Location.objects.get(pk=new_pk)
        if new_location.parent_location:
            new_location_parent = Location.objects.get(pk=asset_references['locations'][old_location_parent.pk])
            new_location.parent_location = new_location_parent

        old_world = old_location.world
        new_world = World.objects.get(pk=asset_references['worlds'][old_world.pk])
        new_location.world = new_world
        new_location.save()

    # go through each chapter and create a reference to its pk,
    # then create the copy of the chapter.
    # go through each section and find those that belong to the
    # old chapter, and create a copy of them going to the new
    # chapter.
    # update the campaign pk along the way.

    for chapter in chapters:

        # create a reference to the chapter's original pk
        old_pk = chapter.pk

        # create a new copy of the chapter
        chapter.pk = None
        chapter.user = user
        chapter.campaign = campaign
        chapter.save()

        replace_content_urls(chapter, asset_references)

        for section in sections:
            # find sections that belong to the chapter
            if section.chapter.pk == old_pk:

                # create a new copy of the section
                section.pk = None
                section.user = user
                section.chapter = chapter
                section.campaign = campaign
                section.save()

                replace_content_urls(section, asset_references)
