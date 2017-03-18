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
def spell_detail(request, spell_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    spells = sorted(models.Spell.objects.filter(user=user), key=lambda spell: spell.name.lower())
    if spell_pk:
        this_spell = get_object_or_404(models.Spell, pk=spell_pk)
        if this_spell.user == request.user:
            return render(request, 'spells/spell_detail.html', {'this_spell': this_spell, 'spells': spells})
        else:
            raise Http404
    elif len(spells) > 0:
        this_spell = spells[0]
        if this_spell.user == request.user:
            return render(request, 'spells/spell_detail.html', {'this_spell': this_spell, 'spells': spells})
        else:
            raise Http404
    else:
        this_spell = None
    return render(request, 'spells/spell_detail.html', {'this_spell': this_spell, 'spells': spells})

@login_required
def spell_create(request):
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    spells_raw = models.Spell.objects.filter(user=request.user).order_by('name')
    spells = {}
    for spell in spells_raw:
        spells[spell.pk] = spell.name
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
    form = forms.SpellForm()
    if request.method == 'POST':
        form = forms.SpellForm(request.POST)
        if form.is_valid():
            spell = form.save(commit=False)
            spell.user = request.user
            spell.save()
            messages.add_message(request, messages.SUCCESS, "Spell created!")
            return HttpResponseRedirect(spell.get_absolute_url())
    return render(request, 'spells/spell_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'spells': spells, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def spell_update(request, spell_pk):
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    spells_raw = models.Spell.objects.filter(user=request.user).order_by('name')
    spells = {}
    for spell in spells_raw:
        spells[spell.pk] = spell.name
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
    spell = get_object_or_404(models.Spell, pk=spell_pk)
    if spell.user == request.user:
        form = forms.SpellForm(instance=spell)
        if request.method == 'POST':
            form = forms.SpellForm(instance=spell, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated spell/spell: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(spell.get_absolute_url())
    else:
        raise Http404
    return render(request, 'spells/spell_form.html', {'form': form, 'spell': spell, 'monsters': monsters, 'npcs': npcs, 'spells': spells, 'players': players, 'worlds': worlds, 'locations': locations})

@login_required
def spell_delete(request, spell_pk):
    spell = get_object_or_404(models.Spell, pk=spell_pk)
    if spell.user == request.user:
        form = forms.DeleteSpellForm(instance=spell)
        if request.method == 'POST':
            form = forms.DeleteSpellForm(request.POST, instance=spell)
            if spell.user.pk == request.user.pk:
                spell.delete()
                messages.add_message(request, messages.SUCCESS, "Spell deleted!")
                return HttpResponseRedirect(reverse('spells:spell_detail'))
    else:
        raise Http404
    return render(request, 'spells/spell_delete.html', {'form': form, 'spell': spell})

@login_required
def spell_copy(request, spell_pk):
    spell = get_object_or_404(models.Spell, pk=spell_pk)
    if spell.user == request.user:
        form = forms.CopySpellForm(instance=spell)
        if request.method == 'POST':
            form = forms.CopySpellForm(request.POST, instance=spell)
            if spell.user.pk == request.user.pk:
                spell.pk = None
                spell.name = spell.name + "_Copy"
                spell.save()
                messages.add_message(request, messages.SUCCESS, "Spell copied!")
                return HttpResponseRedirect(spell.get_absolute_url())
    else:
        raise Http404
    return render(request, 'spells/spell_copy.html', {'form': form, 'spell': spell})
