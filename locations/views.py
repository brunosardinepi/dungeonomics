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
    worlds = sorted(models.World.objects.filter(user=request.user), key=lambda world: world.name.lower())
    if world_pk:
        this_world = get_object_or_404(models.World, pk=world_pk)
        if this_world.user == request.user:
            return render(request, 'locations/location_detail.html', {'this_world': this_world, 'worlds': worlds})
        else:
            raise Http404
    elif location_pk:
        this_location = get_object_or_404(models.Location, pk=location_pk)
        if this_location.user == request.user:
            return render(request, 'locations/location_detail.html', {'this_location': this_location, 'worlds': worlds})
        else:
            raise Http404
    else:
        this_world = None
        if len(worlds) > 0:
            this_world = worlds[0]
        return render(request, 'locations/location_detail.html', {'this_world': this_world, 'worlds': worlds})

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
    worlds_raw = models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    form = forms.WorldForm()
    if request.method == 'POST':
        form = forms.WorldForm(request.POST)
        if form.is_valid():
            world = form.save(commit=False)
            world.user = request.user
            world.save()
            messages.add_message(request, messages.SUCCESS, "World created!")
            return HttpResponseRedirect(world.get_absolute_url())
    return render(request, 'locations/world_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def location_create(request, world_pk, location_pk=None):
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
    worlds_raw = models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        form = forms.LocationForm(world.pk)
        if request.method == 'POST':
            form = forms.LocationForm(world.pk, request.POST)
            if form.is_valid():
                location = form.save(commit=False)
                if location_pk:
                    parent_location = get_object_or_404(models.Location, pk=location_pk)
                    if parent_location.user == request.user:
                        location.parent = parent_location
                location.user = request.user
                location.world = world
                location.save()
                messages.add_message(request, messages.SUCCESS, "Location created!")
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'world': world, 'worlds': worlds,'locations': locations})

@login_required
def world_update(request, world_pk):
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
    worlds_raw = models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    world = get_object_or_404(models.World, pk=world_pk)
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
    return render(request, 'locations/world_form.html', {'form': form, 'formset': location_forms, 'world': world, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def location_update(request, location_pk):
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
    worlds_raw = models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    location = get_object_or_404(models.Location, pk=location_pk)
    if location.user == request.user:
        form = forms.LocationForm(location.world.pk, location_pk, instance=location)
        if request.method == 'POST':
            form = forms.LocationForm(location.world.pk, location_pk, request.POST, instance=location)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated location: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'world': location.world, 'location': location, 'worlds': worlds,'locations': locations})

@login_required
def world_delete(request, world_pk):
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        form = forms.DeleteWorldForm(instance=world)
        if request.method == 'POST':
            form = forms.DeleteWorldForm(request.POST, instance=world)
            if world.user.pk == request.user.pk:
                world.delete()
                messages.add_message(request, messages.SUCCESS, "World deleted!")
                return HttpResponseRedirect(reverse('locations:location_detail'))
    else:
        raise Http404
    return render(request, 'locations/world_delete.html', {'form': form, 'world': world})

@login_required
def location_delete(request, location_pk):
    location = get_object_or_404(models.Location, pk=location_pk)
    form = forms.DeleteLocationForm(instance=location)
    if request.method == 'POST':
        form = forms.DeleteLocationForm(request.POST, instance=location)
        if location.user.pk == request.user.pk:
            location.delete()
            messages.add_message(request, messages.SUCCESS, "Location deleted!")
            return HttpResponseRedirect(reverse('locations:location_detail'))
    return render(request, 'locations/location_delete.html', {'form': form, 'location': location})
