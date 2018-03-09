from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from itertools import chain

from . import forms
from . import models

from items import models as item_models
from locations import models as location_models

import json


@login_required
def monster_detail(request, monster_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monster_pk:
        monster = get_object_or_404(models.Monster, pk=monster_pk)
        if monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'monster': monster, 'monsters': monsters})
        else:
            raise Http404
    elif len(monsters) > 0:
        monster = monsters[0]
        if monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'monster': monster, 'monsters': monsters})
        else:
            raise Http404
    else:
        monster = None
    return render(request, 'characters/monster_detail.html', {'monster': monster, 'monsters': monsters})

@login_required
def npc_detail(request, npc_pk=''):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npc_pk:
        npc = get_object_or_404(models.NPC, pk=npc_pk)
        if npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'npc': npc, 'npcs': npcs})
        else:
            raise Http404
    elif len(npcs) > 0:
        npc = npcs[0]
        if npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'npc': npc, 'npcs': npcs})
        else:
            raise Http404
    else:
        npc = None
    return render(request, 'characters/npc_detail.html', {'npc': npc, 'npcs': npcs})

@login_required
def player_detail(request, player_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    players = sorted(models.Player.objects.filter(user=user),
        key=lambda player: player.player_name.lower()
        )
    if player_pk:
        player = get_object_or_404(models.Player, pk=player_pk)
        if player.user == request.user:
            return render(request, 'characters/player_detail.html', {'player': player, 'players': players})
        else:
            raise Http404
    elif len(players) > 0:
        player = players[0]
        if player.user == request.user:
            return render(request, 'characters/player_detail.html', {'player': player, 'players': players})
        else:
            raise Http404
    else:
        player = None
    return render(request, 'characters/player_detail.html', {'player': player, 'players': players})

@login_required
def monster_create(request):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    form = forms.MonsterForm()
    if request.method == 'POST':
        form = forms.MonsterForm(request.POST)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.user = request.user
            monster.save()
            messages.add_message(request, messages.SUCCESS, "Monster created!")
            return HttpResponseRedirect(monster.get_absolute_url())
    return render(request, 'characters/monster_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def npc_create(request):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    form = forms.NPCForm()
    if request.method == 'POST':
        form = forms.NPCForm(request.POST)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.user = request.user
            npc.save()
            messages.add_message(request, messages.SUCCESS, "NPC created!")
            return HttpResponseRedirect(npc.get_absolute_url())
    return render(request, 'characters/npc_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def player_create(request):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    form = forms.PlayerForm()
    if request.method == 'POST':
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.add_message(request, messages.SUCCESS, "Player created!")
            return HttpResponseRedirect(player.get_absolute_url())
    return render(request, 'characters/player_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def monster_update(request, monster_pk):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.MonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.MonsterForm(instance=monster, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated monster: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(monster.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/monster_form.html', {'form': form, 'monster': monster, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def npc_update(request, npc_pk):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.NPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.NPCForm(instance=npc, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated NPC: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(npc.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/npc_form.html', {'form': form, 'npc': npc, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def player_update(request, player_pk):
    monsters_raw = models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = models.Player.objects.filter(user=request.user).order_by('player_name')
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
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.PlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.PlayerForm(instance=player, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated player")
                return HttpResponseRedirect(player.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/player_form.html', {'form': form, 'player': player, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def monster_delete(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        monster.delete()
        messages.success(request, 'Monster deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('characters:monster_detail'))
    else:
        raise Http404

@login_required
def npc_delete(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        npc.delete()
        messages.success(request, 'NPC deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('characters:npc_detail'))
    else:
        raise Http404

@login_required
def player_delete(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        player.delete()
        messages.success(request, 'Player deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('characters:player_detail'))
    else:
        raise Http404

@login_required
def monster_copy(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.CopyMonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.CopyMonsterForm(request.POST, instance=monster)
            if monster.user.pk == request.user.pk:
                monster.pk = None
                monster.name = monster.name + "_Copy"
                monster.save()
                messages.add_message(request, messages.SUCCESS, "Monster Copied!")
                return HttpResponseRedirect(monster.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/monster_copy.html', {'form': form, 'monster': monster})


@login_required
def npc_copy(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.CopyNPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.CopyNPCForm(request.POST, instance=npc)
            if npc.user.pk == request.user.pk:
                npc.pk = None
                npc.name = npc.name + "_Copy"
                npc.save()
                messages.add_message(request, messages.SUCCESS, "NPC copied!")
                return HttpResponseRedirect(npc.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/npc_copy.html', {'form': form, 'npc': npc})


@login_required
def player_copy(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.CopyPlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.CopyPlayerForm(request.POST, instance=player)
            if player.user.pk == request.user.pk:
                player.pk = None
                player.player_name = player.player_name + "_Copy"
                player.save()
                messages.add_message(request, messages.SUCCESS, "Player copied!")
                return HttpResponseRedirect(player.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/player_copy.html', {'form': form, 'player': player})

@login_required
def monster_import(request):
    user_import = None
    form = forms.ImportMonsterForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportMonsterForm(request.POST)
        if "monsters" in user_import: 
            for monster, monster_attributes in user_import["monsters"].items():
                new_monster = models.Monster(
                    user=request.user,
                    name=monster,
                    alignment=monster_attributes["alignment"],
                    size=monster_attributes["size"],
                    languages=monster_attributes["languages"],
                    strength=monster_attributes["strength"],
                    dexterity=monster_attributes["dexterity"],
                    constitution=monster_attributes["constitution"],
                    intelligence=monster_attributes["intelligence"],
                    wisdom=monster_attributes["wisdom"],
                    charisma=monster_attributes["charisma"],
                    armor_class=monster_attributes["armor_class"],
                    hit_points=monster_attributes["hit_points"],
                    speed=monster_attributes["speed"],
                    saving_throws=monster_attributes["saving_throws"],
                    skills=monster_attributes["skills"],
                    creature_type=monster_attributes["creature_type"],
                    damage_vulnerabilities=monster_attributes["damage_vulnerabilities"],
                    damage_immunities=monster_attributes["damage_immunities"],
                    damage_resistances=monster_attributes["damage_resistances"],
                    condition_immunities=monster_attributes["condition_immunities"],
                    senses=monster_attributes["senses"],
                    challenge_rating=monster_attributes["challenge_rating"],
                    traits=monster_attributes["traits"],
                    actions=monster_attributes["actions"],
                    notes=monster_attributes["notes"]
                )
                new_monster.save()
            return HttpResponseRedirect(reverse('characters:monster_detail'))
    return render(request, 'characters/monster_import.html', {'form': form, 'user_import': user_import})

@login_required
def npc_import(request):
    user_import = None
    form = forms.ImportNPCForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportNPCForm(request.POST)
        if "npcs" in user_import:
            for npc, npc_attributes in user_import["npcs"].items():
                new_npc = models.NPC(
                    user=request.user,
                    name=npc,
                    alignment=npc_attributes["alignment"],
                    size=npc_attributes["size"],
                    languages=npc_attributes["languages"],
                    strength=npc_attributes["strength"],
                    dexterity=npc_attributes["dexterity"],
                    constitution=npc_attributes["constitution"],
                    intelligence=npc_attributes["intelligence"],
                    wisdom=npc_attributes["wisdom"],
                    charisma=npc_attributes["charisma"],
                    armor_class=npc_attributes["armor_class"],
                    hit_points=npc_attributes["hit_points"],
                    speed=npc_attributes["speed"],
                    saving_throws=npc_attributes["saving_throws"],
                    skills=npc_attributes["skills"],
                    npc_class=npc_attributes["npc_class"],
                    age=npc_attributes["age"],
                    height=npc_attributes["height"],
                    weight=npc_attributes["weight"],
                    creature_type=npc_attributes["creature_type"],
                    damage_vulnerabilities=npc_attributes["damage_vulnerabilities"],
                    damage_immunities=npc_attributes["damage_immunities"],
                    damage_resistances=npc_attributes["damage_resistances"],
                    condition_immunities=npc_attributes["condition_immunities"],
                    senses=npc_attributes["senses"],
                    challenge_rating=npc_attributes["challenge_rating"],
                    traits=npc_attributes["traits"],
                    actions=npc_attributes["actions"],
                    notes=npc_attributes["notes"]
                )
                new_npc.save()
        return HttpResponseRedirect(reverse('characters:npc_detail'))
    return render(request, 'characters/npc_import.html', {'form': form, 'user_import': user_import})

@login_required
def monster_export(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monsters:
        for monster in monsters:
            monster.traits = json.dumps(monster.traits)
            monster.actions = json.dumps(monster.actions)
            monster.notes = json.dumps(monster.notes)
        return render(request, 'characters/monster_export.html', {'monsters': monsters})
    else:
        raise Http404

@login_required
def npc_export(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npcs:
        for npc in npcs:
            npc.traits = json.dumps(npc.traits)
            npc.actions = json.dumps(npc.actions)
            npc.notes = json.dumps(npc.notes)
        return render(request, 'characters/npc_export.html', {'npcs': npcs})
    else:
        raise Http404

@login_required
def monster_srd(request):
    form = forms.SRDMonsterForm()
    monsters = sorted(models.Monster.objects.filter(user=3029),
        key=lambda monster: monster.name.lower()
        )
    if request.method == 'POST':
        form = forms.MonsterForm(request.POST)
        selected_monsters = []
        for monster_pk in request.POST.getlist('monster'):
            monster = models.Monster.objects.get(pk=monster_pk)
            selected_monsters.append(monster)
        empty_queryset = models.Monster.objects.none()
        monster_queryset = list(chain(empty_queryset, selected_monsters))
        for monster in monster_queryset:
            monster.traits = json.dumps(monster.traits)
            monster.actions = json.dumps(monster.actions)
            monster.notes = json.dumps(monster.notes)
        return render(request, 'characters/monster_export.html', {'monsters': monster_queryset})
    return render(request, 'characters/monster_srd_form.html', {'form': form, 'monsters': monsters})

@login_required
def npc_srd(request):
    form = forms.SRDNPCForm()
    npcs = sorted(models.NPC.objects.filter(user=3029),
        key=lambda npc: npc.name.lower()
        )
    if request.method == 'POST':
        form = forms.NPCForm(request.POST)
        selected_npcs = []
        for npc_pk in request.POST.getlist('npc'):
            npc = models.NPC.objects.get(pk=npc_pk)
            selected_npcs.append(npc)
        empty_queryset = models.NPC.objects.none()
        npc_queryset = list(chain(empty_queryset, selected_npcs))
        for npc in npc_queryset:
            npc.traits = json.dumps(npc.traits)
            npc.actions = json.dumps(npc.actions)
            npc.notes = json.dumps(npc.notes)
        return render(request, 'characters/npc_export.html', {'npcs': npc_queryset})
    return render(request, 'characters/npc_srd_form.html', {'form': form, 'npcs': npcs})

@login_required
def monsters_delete(request):
    form = forms.DeleteMonsterForm()
    monsters = sorted(models.Monster.objects.filter(user=request.user),
        key=lambda monster: monster.name.lower()
        )
    if request.method == 'POST':
        form = forms.DeleteMonsterForm(request.POST)
        selected_monsters = []
        for monster_pk in request.POST.getlist('monster'):
            monster = models.Monster.objects.get(pk=monster_pk)
            selected_monsters.append(monster)
        empty_queryset = models.Monster.objects.none()
        monster_queryset = list(chain(empty_queryset, selected_monsters))
        for monster in monster_queryset:
            monster.delete()
        return HttpResponseRedirect(reverse('characters:monster_detail'))
    return render(request, 'characters/monsters_delete.html', {'form': form, 'monsters': monsters})

@login_required
def npcs_delete(request):
    form = forms.DeleteNPCForm()
    npcs = sorted(models.NPC.objects.filter(user=request.user),
        key=lambda npc: npc.name.lower()
        )
    if request.method == 'POST':
        form = forms.DeleteNPCForm(request.POST)
        selected_npcs = []
        for npc_pk in request.POST.getlist('npc'):
            npc = models.NPC.objects.get(pk=npc_pk)
            selected_npcs.append(npc)
        empty_queryset = models.NPC.objects.none()
        npc_queryset = list(chain(empty_queryset, selected_npcs))
        for npc in npc_queryset:
            npc.delete()
        return HttpResponseRedirect(reverse('characters:npc_detail'))
    return render(request, 'characters/npcs_delete.html', {'form': form, 'npcs': npcs})


