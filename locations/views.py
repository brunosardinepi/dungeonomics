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
def location_detail(request, location_pk=None):
    locations = sorted(models.Location.objects.filter(user=request.user), key=lambda location: location.name.lower())
    if location_pk:
        this_location = get_object_or_404(models.Location, pk=location_pk)
        if this_location.user == request.user:
            return render(request, 'locations/location_detail.html', {'this_location': this_location, 'locations': locations})
        else:
            raise Http404
    else:
        user = None
        if request.user.is_authenticated():
            user = request.user.pk
        if len(locations) > 0:
            this_location = locations[0]
        else:
            this_location = None
        return render(request, 'locations/location_detail.html', {'this_location': this_location, 'locations': locations})

@login_required
def location_create(request, location_pk=None):
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
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    form = forms.LocationForm()
    if request.method == 'POST':
        form = forms.LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            if location_pk:
                parent_location = get_object_or_404(models.Location, pk=location_pk)
                if parent_location.user == request.user:
                    location.parent = parent_location
            location.user = request.user
            location.save()
            messages.add_message(request, messages.SUCCESS, "Location created!")
            return HttpResponseRedirect(location.get_absolute_url())
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'locations': locations})

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
    locations_raw = models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name

    location = get_object_or_404(models.Location, pk=location_pk)
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
    return render(request, 'locations/location_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'world': location.world, 'location': location, 'locations': locations})

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
