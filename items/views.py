from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from . import forms
from . import models

from characters import models as character_models
from locations import models as location_models


@login_required
def item_detail(request, item_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    items = sorted(models.Item.objects.filter(user=user), key=lambda item: item.name.lower())
    if item_pk:
        this_item = get_object_or_404(models.Item, pk=item_pk)
        if this_item.user == request.user:
            return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})
        else:
            raise Http404
    elif len(items) > 0:
        this_item = items[0]
        if this_item.user == request.user:
            return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})
        else:
            raise Http404
    else:
        this_item = None
    return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})

@login_required
def item_create(request):
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    worlds_raw = location_models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = location_models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    form = forms.ItemForm()
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item created!")
            return HttpResponseRedirect(item.get_absolute_url())
    return render(request, 'items/item_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def item_update(request, item_pk):
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = character_models.Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    worlds_raw = location_models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = location_models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        form = forms.ItemForm(instance=item)
        if request.method == 'POST':
            form = forms.ItemForm(instance=item, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated item: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    return render(request, 'items/item_form.html', {'form': form, 'item': item, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def item_delete(request, item_pk):
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        form = forms.DeleteItemForm(instance=item)
        if request.method == 'POST':
            form = forms.DeleteItemForm(request.POST, instance=item)
            if item.user.pk == request.user.pk:
                item.delete()
                messages.add_message(request, messages.SUCCESS, "Item deleted!")
                return HttpResponseRedirect(reverse('items:item_detail'))
    else:
        raise Http404
    return render(request, 'items/item_delete.html', {'form': form, 'item': item})

@login_required
def item_copy(request, item_pk):
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        form = forms.CopyItemForm(instance=item)
        if request.method == 'POST':
            form = forms.CopyItemForm(request.POST, instance=item)
            if item.user.pk == request.user.pk:
                item.pk = None
                item.name = item.name + "_Copy"
                item.save()
                messages.add_message(request, messages.SUCCESS, "Item copied!")
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    return render(request, 'items/item_copy.html', {'form': form, 'item': item})
