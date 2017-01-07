from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models
from characters import models as character_models
from items import models as item_models

import json


@login_required
def location_detail(request, world_pk=None, location_pk=None):
    worlds = sorted(models.World.objects.filter(user=request.user), key=lambda world: world.name)
    locations = []
    for world in worlds:
        locations.append(sorted(
            models.Location.objects.filter(world=world),
            key=lambda location: location.name
            ))
    locations = [item for sublist in locations for item in sublist]

    if world_pk:
        this_world = get_object_or_404(models.World, pk=world_pk)
        if this_world.user == request.user:
            if location_pk:
                this_location = get_object_or_404(models.Location, pk=location_pk)
                return render(request, 'locations/location_detail.html', {'this_world': this_world, 'this_location': this_location, 'worlds': worlds, 'locations': locations})
            else:
                return render(request, 'locations/location_detail.html', {'this_world': this_world, 'worlds': worlds, 'locations': locations})
        else:
            raise Http404
    else:
        this_world = None
        user = None
        if request.user.is_authenticated():
            user = request.user.pk
        if len(worlds) > 0:
            this_world = worlds[0]
        return render(request, 'locations/location_detail.html', {'this_world': this_world, 'worlds': worlds, 'locations': locations})

@login_required
def world_create(request):
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name

    form = forms.WorldForm()
    if request.method == 'POST':
        form = forms.WorldForm(request.POST)
        if form.is_valid():
            world = form.save(commit=False)
            world.user = request.user
            world.save()
            messages.add_message(request, messages.SUCCESS, "World created!")
            return HttpResponseRedirect(world.get_absolute_url())
    return render(request, 'locations/world_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players})

@login_required
def location_create(request, world_pk):
    world = get_object_or_404(models.World, pk=world_pk)
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    if world.user == request.user:
        form = forms.LocationForm()
        if request.method == 'POST':
            form = forms.LocationForm(request.POST)
            if form.is_valid():
                location = form.save(commit=False)
                location.user = request.user
                location.world = world
                location.save()
                messages.add_message(request, messages.SUCCESS, "Location created!")
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'world': world})

@login_required
def world_update(request, world_pk):
    world = get_object_or_404(models.World, pk=world_pk)
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    if world.user == request.user:
        form = forms.WorldForm(instance=world)
        location_forms = forms.LocationInlineFormSet(queryset=form.instance.location_set.all())
        if request.method == 'POST':
            form = forms.WorldForm(request.POST, instance=world)
            location_forms = forms.LocationInlineFormSet(request.POST, queryset=form.instance.location_set.all())
            if form.is_valid() and location_forms.is_valid():
                form.save()
                locations = location_forms.save(commit=False)
                for location in locations:
                    location.world = world
                    location.user = request.user
                    location.save()
                for location in location_forms.deleted_objects:
                    location.delete()
                messages.add_message(request, messages.SUCCESS, "Updated world: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(world.get_absolute_url())
    else:
        raise Http404
    return render(request, 'locations/world_form.html', {'form': form, 'formset': location_forms, 'world': world, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players})

@login_required
def location_update(request, world_pk, location_pk):
    location = get_object_or_404(models.Location, pk=location_pk, world_id=world_pk)
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    if location.user == request.user:
        form = forms.LocationForm(instance=location)
        if request.method == 'POST':
            form = forms.LocationForm(request.POST, instance=location)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated location: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'world': location.world, 'location': location})

@login_required
def world_delete(request, world_pk):
    world = get_object_or_404(models.world, pk=world_pk)
    if world.user == request.user:
        form = forms.DeleteWorldForm(instance=world)
        if request.method == 'POST':
            form = forms.DeleteWorldForm(request.POST, instance=world)
            if world.user.pk == request.user.pk:
                world.delete()
                messages.add_message(request, messages.SUCCESS, "World deleted!")
                return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404
    return render(request, 'locations/world_delete.html', {'form': form, 'world': world})


@login_required
def location_delete(request, world_pk, location_pk):
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        location = get_object_or_404(models.Location, pk=location_pk)
        form = forms.DeleteLocationForm(instance=location)
        if request.method == 'POST':
            form = forms.DeleteLocationForm(request.POST, instance=location)
            if location.user.pk == request.user.pk:
                location.delete()
                messages.add_message(request, messages.SUCCESS, "Location deleted!")
                return HttpResponseRedirect(reverse('locations:location_detail', kwargs={'world_pk': world.pk}))
    else:
        raise Http404
    return render(request, 'locations/location_delete.html', {'form': form, 'location': location})

# @login_required
# def campaign_import(request):
#     user_import = None
#     form = forms.ImportCampaignForm()
#     if request.method == 'POST':
#         if request.POST.get('user_import'):
#             user_import = request.POST.get('user_import')
#             user_import = json.loads(user_import, strict=False)
#         else:
#             return Http404
#         form = forms.ImportCampaignForm(request.POST)
#         if form.is_valid():
#             campaign = form.save(commit=False)
#             campaign.user = request.user
#             campaign.save()
#             for chapter_order, chapter_attributes in user_import["chapters"].items():
#                 new_chapter = models.Chapter(
#                     title=chapter_attributes["title"],
#                     user=request.user,
#                     campaign=campaign,
#                     order=chapter_order,
#                     content=chapter_attributes["content"]
#                     )
#                 new_chapter.save()
#                 if "sections" in chapter_attributes:
#                     for section_order, section_attributes in chapter_attributes["sections"].items():
#                         new_section = models.Section(
#                             title=section_attributes["title"],
#                             user=request.user,
#                             campaign=campaign,
#                             chapter=new_chapter,
#                             order=section_order,
#                             content=section_attributes["content"]
#                             )
#                         new_section.save()
#             if "monsters" in user_import: 
#                 for monster, monster_attributes in user_import["monsters"].items():
#                     new_monster = character_models.Monster(
#                         user=request.user,
#                         name=monster,
#                         alignment=monster_attributes["alignment"],
#                         size=monster_attributes["size"],
#                         languages=monster_attributes["languages"],
#                         strength=monster_attributes["strength"],
#                         dexterity=monster_attributes["dexterity"],
#                         constitution=monster_attributes["constitution"],
#                         intelligence=monster_attributes["intelligence"],
#                         wisdom=monster_attributes["wisdom"],
#                         charisma=monster_attributes["charisma"],
#                         armor_class=monster_attributes["armor_class"],
#                         hit_points=monster_attributes["hit_points"],
#                         speed=monster_attributes["speed"],
#                         saving_throws=monster_attributes["saving_throws"],
#                         skills=monster_attributes["skills"],
#                         creature_type=monster_attributes["creature_type"],
#                         damage_vulnerabilities=monster_attributes["damage_vulnerabilities"],
#                         damage_immunities=monster_attributes["damage_immunities"],
#                         damage_resistances=monster_attributes["damage_resistances"],
#                         condition_immunities=monster_attributes["condition_immunities"],
#                         senses=monster_attributes["senses"],
#                         challenge_rating=monster_attributes["challenge_rating"],
#                         traits=monster_attributes["traits"],
#                         actions=monster_attributes["actions"],
#                         notes=monster_attributes["notes"]
#                     )
#                     new_monster.save()
#             if "npcs" in user_import:
#                 for npc, npc_attributes in user_import["npcs"].items():
#                     new_npc = character_models.NPC(
#                         user=request.user,
#                         name=npc,
#                         alignment=npc_attributes["alignment"],
#                         size=npc_attributes["size"],
#                         languages=npc_attributes["languages"],
#                         strength=npc_attributes["strength"],
#                         dexterity=npc_attributes["dexterity"],
#                         constitution=npc_attributes["constitution"],
#                         intelligence=npc_attributes["intelligence"],
#                         wisdom=npc_attributes["wisdom"],
#                         charisma=npc_attributes["charisma"],
#                         armor_class=npc_attributes["armor_class"],
#                         hit_points=npc_attributes["hit_points"],
#                         speed=npc_attributes["speed"],
#                         saving_throws=npc_attributes["saving_throws"],
#                         skills=npc_attributes["skills"],
#                         npc_class=npc_attributes["npc_class"],
#                         age=npc_attributes["age"],
#                         height=npc_attributes["height"],
#                         weight=npc_attributes["weight"],
#                         creature_type=npc_attributes["creature_type"],
#                         damage_vulnerabilities=npc_attributes["damage_vulnerabilities"],
#                         damage_immunities=npc_attributes["damage_immunities"],
#                         damage_resistances=npc_attributes["damage_resistances"],
#                         condition_immunities=npc_attributes["condition_immunities"],
#                         senses=npc_attributes["senses"],
#                         challenge_rating=npc_attributes["challenge_rating"],
#                         traits=npc_attributes["traits"],
#                         actions=npc_attributes["actions"],
#                         notes=npc_attributes["notes"]
#                     )
#                     new_npc.save()
#             if "items" in user_import:
#                 for item, item_attributes in user_import["items"].items():
#                     new_item = item_models.Item(
#                         user=request.user,
#                         name=item,
#                         item_type=item_attributes["item_type"],
#                         rarity=item_attributes["rarity"],
#                         description=item_attributes["description"]
#                     )
#                     new_item.save()
#             return HttpResponseRedirect(campaign.get_absolute_url())
#     return render(request, 'campaign/campaign_import.html', {'form': form, 'user_import': user_import})

# @login_required
# def campaign_export(request, campaign_pk):
#     if campaign_pk:
#         campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
#         chapters = sorted(models.Chapter.objects.filter(campaign=campaign),
#             key=lambda chapter: chapter.order
#             )
#         monsters = sorted(character_models.Monster.objects.filter(user=request.user),
#             key=lambda monster: monster.name.lower()
#             )
#         npcs = sorted(character_models.NPC.objects.filter(user=request.user),
#             key=lambda npc: npc.name.lower()
#             )
#         items = sorted(item_models.Item.objects.filter(user=request.user),
#             key=lambda item: item.name.lower()
#             )
#         for chapter in chapters:
#             chapter.content = json.dumps(chapter.content)
#         for monster in monsters:
#             monster.traits = json.dumps(monster.traits)
#             monster.actions = json.dumps(monster.actions)
#             monster.notes = json.dumps(monster.notes)
#         for npc in npcs:
#             npc.traits = json.dumps(npc.traits)
#             npc.actions = json.dumps(npc.actions)
#             npc.notes = json.dumps(npc.notes)
#         for item in items:
#             item.description = json.dumps(item.description)
#         return render(request, 'campaign/campaign_export.html', {'campaign': campaign, 'chapters': chapters, 'monsters': monsters, 'npcs': npcs, 'items': items})
#     else:
#         raise Http404