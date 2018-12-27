from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from campaign.models import Campaign, Chapter, Section
from characters.models import Monster, NPC, Player
from items.models import Item
from locations.models import Location, World
from posts.models import Post
from tables.models import Table
from tavern.models import Review


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

def campaign_context(request, data={}, campaign_pk=None, chapter_pk=None, section_pk=None):
    ### CAMPAIGN
    # get the user's campaigns
    campaigns = Campaign.objects.filter(user=request.user).order_by('title')

    # if a campaign was specified, get the campaign based on pk from url
    if campaign_pk:
        campaign = get_object_or_404(Campaign, pk=campaign_pk)

    # if the user has campaigns, get the first one
    elif len(campaigns) > 0:
        campaign = campaigns[0]

    # this user has no campaigns
    else:
        campaign = None

    # if there's a campaign, get the campaign party's five most recent posts
    if campaign:
        posts = Post.objects.filter(campaign=campaign).order_by('-date')[:5]
        data['posts'] = posts

    # check if the viewer is the campaign owner
    if campaign.user == request.user:

        ### CHAPTER
        # get the chapters for this campaign, sorted by chapter order
        chapters = Chapter.objects.filter(campaign=campaign).order_by('order')

        # if a chapter was specified, get the chapter based on the pk from url
        if chapter_pk:
            chapter = get_object_or_404(Chapter, pk=chapter_pk)

        # user didn't specify a chapter, so get the first one
        elif len(chapters) > 0:
            chapter = chapters[0]

        # there are no chapters
        else:
            chapter = None

        ### SECTION
        sections = []
        for c in chapters:
            # get the sections for each chapter and append to the list
            sections.append(Section.objects.filter(chapter=c).order_by('order'))

        # can't remember what i'm doing here, maybe merging into a single list
        sections = [item for sublist in sections for item in sublist]

        # if a section was specified, get the section based on the pk from url
        if section_pk:
            section = get_object_or_404(Section, pk=section_pk)

        # no section was specified
        else:
            section = None

        # return all our data in a dictionary with the appropriate key/value pairs
        data['campaigns'] = campaigns
        data['campaign'] = campaign
        data['chapter'] = chapter
        data['section'] = section
        data['chapters'] = chapters
        data['sections'] = sections
        return data

    # the viewer is not the campaign owner
    else:
        raise Http404

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
