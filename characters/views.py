from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from itertools import chain

from . import forms
from . import models
from campaign.models import Campaign
from characters.utils import get_character_object
from dungeonomics.utils import at_tagging
from dungeonomics import character_suggested_attributes
from items import models as item_models
from locations import models as location_models
from tavern.models import Review
from tavern.utils import rating_stars_html

import json


@login_required
def monster_detail(request, monster_pk=None):
    user = None
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
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
    data = at_tagging(request)
    form = forms.MonsterForm()
    if request.method == 'POST':
        form = forms.MonsterForm(request.POST)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.user = request.user
            monster.save()
            messages.add_message(request, messages.SUCCESS, "Monster created!")
            return HttpResponseRedirect(monster.get_absolute_url())
    data['form'] = form
    return render(request, 'characters/monster_form.html', data)

@login_required
def npc_create(request):
    data = at_tagging(request)
    form = forms.NPCForm()
    if request.method == 'POST':
        form = forms.NPCForm(request.POST)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.user = request.user
            npc.save()
            messages.add_message(request, messages.SUCCESS, "NPC created!")
            return HttpResponseRedirect(npc.get_absolute_url())
    data['form'] = form
    return render(request, 'characters/npc_form.html', data)

@login_required
def player_create(request):
    data = at_tagging(request)
    form = forms.PlayerForm()
    if request.method == 'POST':
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.add_message(request, messages.SUCCESS, "Player created!")
            return HttpResponseRedirect(player.get_absolute_url())
    data['form'] = form
    return render(request, 'characters/player_form.html', data)

@login_required
def monster_update(request, monster_pk):
    data = at_tagging(request)
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
    data['monster'] = monster
    data['form'] = form
    return render(request, 'characters/monster_form.html', data)

@login_required
def npc_update(request, npc_pk):
    data = at_tagging(request)
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
    data['npc'] = npc
    data['form'] = form
    return render(request, 'characters/npc_form.html', data)

@login_required
def player_update(request, player_pk):
    data = at_tagging(request)
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
    data['player'] = player
    data['form'] = form
    return render(request, 'characters/player_form.html', data)

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
                messages.add_message(request, messages.SUCCESS, "Monster copied!")
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

            for obj in serializers.deserialize("json", user_import):
                obj.object.pk = None
                obj.object.user = request.user
                obj.object.save()
            return HttpResponseRedirect(reverse('characters:monster_detail'))
        else:
            return Http404
    return render(request, 'characters/monster_import.html', {'form': form})

@login_required
def npc_import(request):
    user_import = None
    form = forms.ImportNPCForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')

            for obj in serializers.deserialize("json", user_import):
                obj.object.pk = None
                obj.object.user = request.user
                obj.object.save()
            return HttpResponseRedirect(reverse('characters:npc_detail'))
        else:
            return Http404
    return render(request, 'characters/npc_import.html', {'form': form})

@login_required
def monster_export(request):
    user = None
    if request.user.is_authenticated:
        user = request.user.pk

    queryset = models.Monster.objects.filter(user=user).order_by('name')
    monsters = serializers.serialize("json", queryset, indent=2)

    if monsters:
        return render(request, 'characters/monster_export.html', {'monsters': monsters})
    else:
        raise Http404

@login_required
def npc_export(request):
    user = None
    if request.user.is_authenticated:
        user = request.user.pk

    queryset = models.NPC.objects.filter(user=user).order_by('name')
    npcs = serializers.serialize("json", queryset, indent=2)

    if npcs:
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
        monster_queryset = serializers.serialize("json", selected_monsters, indent=2)
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
        npc_queryset = serializers.serialize("json", selected_npcs, indent=2)
        return render(request, 'characters/npc_export.html', {'npcs': npc_queryset})
    return render(request, 'characters/npc_srd_form.html', {'form': form, 'npcs': npcs})


class MonstersDelete(View):
    def get(self, request, *args, **kwargs):
        monsters = models.Monster.objects.filter(user=request.user).order_by('name')
        return render(request, 'characters/monsters_delete.html', {'monsters': monsters})

    def post(self, request, *args, **kwargs):
        for monster_pk in request.POST.getlist('monster'):
            models.Monster.objects.get(pk=monster_pk).delete()
        return HttpResponseRedirect(reverse('characters:monster_detail'))


class NPCsDelete(View):
    def get(self, request, *args, **kwargs):
        npcs = models.NPC.objects.filter(user=request.user).order_by('name')
        return render(request, 'characters/npcs_delete.html', {'npcs': npcs})

    def post(self, request, *args, **kwargs):
        for npc_pk in request.POST.getlist('npc'):
            models.NPC.objects.get(pk=npc_pk).delete()
        return HttpResponseRedirect(reverse('characters:npc_detail'))


class PlayersDelete(View):
    def get(self, request, *args, **kwargs):
        players = models.Player.objects.filter(user=request.user).order_by('name')
        return render(request, 'characters/players_delete.html', {'players': players})

    def post(self, request, *args, **kwargs):
        for player_pk in request.POST.getlist('player'):
            models.Player.objects.get(pk=player_pk).delete()
        return HttpResponseRedirect(reverse('characters:player_detail'))


class PlayerCampaigns(View):
    def get(self, request, player_pk):
        player = get_object_or_404(models.Player, pk=player_pk)
        if request.user == player.user:
            campaigns = player.campaigns.all()
            return render(self.request, 'characters/player_campaigns.html', {
                'player': player,
                'campaigns': campaigns,
            })
        else:
            raise Http404

    def post(self, request, player_pk):
        player = get_object_or_404(models.Player, pk=player_pk)
        if request.user == player.user:
            campaigns = self.request.POST.getlist('campaigns')
            # for each campaign, remove the player
            for pk in campaigns:
                campaign = get_object_or_404(Campaign, pk=pk)
                player.campaigns.remove(campaign)
            messages.add_message(request, messages.SUCCESS, "Player has been removed from campaign(s)")
            return redirect('characters:player_campaigns', player_pk=player.pk)
        else:
            raise Http404

class CharacterDetail(View):
    def get(self, request, *args, **kwargs):
        characters = models.GeneralCharacter.objects.filter(user=request.user).order_by('name')

        try:
            character = models.GeneralCharacter.objects.get(pk=kwargs['pk'])
        except KeyError:
            if characters:
                character = characters[0]
            else:
                character = None

        if character.user == request.user:
            stats = {
                "Strength": 0,
                "Dexterity": 0,
                "Constitution": 0,
                "Intelligence": 0,
                "Wisdom": 0,
                "Charisma": 0,
            }
            for stat, value in stats.items():
                print("stat = {}, value = {}".format(stat, value))
                try:
                    attribute = character.attribute_set.get(name=stat)
                except models.Attribute.DoesNotExist:
                    attribute = None
                stats[stat] = attribute
            print("stats = {}".format(stats))
            return render(request, 'characters/character_detail.html', {
                'characters': characters,
                'character': character,
                'stats': stats,
            })
        raise Http404

class CharacterCreate(View):
    def get(self, request, *args, **kwargs):
        data = at_tagging(request)
        data['form'] = forms.CharacterForm()
        data['formset'] = forms.AttributeFormSet()
        data['suggested_attributes'] = character_suggested_attributes.attrs
        return render(request, 'characters/character_form.html', data)

    def post(self, request, *args, **kwargs):
        form = forms.CharacterForm(request.POST)
        formset = forms.AttributeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()

            attributes = formset.save(commit=False)
            for attribute in attributes:
                attribute.character = character
                attribute.save()

            messages.add_message(request, messages.SUCCESS, "Character created")
            return HttpResponseRedirect(character.get_absolute_url())

@login_required
def character_update(request, pk):
    character = get_object_or_404(models.GeneralCharacter, pk=pk)
    if character.user == request.user:
        form = forms.CharacterForm(instance=character)
        formset = forms.AttributeFormSet(instance=character)
        if request.method == 'POST':
            form = forms.CharacterForm(request.POST, instance=character)
            formset = forms.AttributeFormSet(request.POST, instance=character)
            if form.is_valid() and formset.is_valid():
                form.save()
                attributes = formset.save(commit=False)
                for attribute in attributes:
                    attribute.character = character
                    attribute.save()
                for attribute in formset.deleted_objects:
                    attribute.delete()
                messages.add_message(request,
                    messages.SUCCESS,
                    "Updated character: {}".format(form.cleaned_data['name'])
                )
                return HttpResponseRedirect(character.get_absolute_url())
    else:
        raise Http404
    data = at_tagging(request)
    data['suggested_attributes'] = character_suggested_attributes.attrs
    data['form'] = form
    data['formset'] = formset
    data['character'] = character
    return render(request, 'characters/character_form.html', data)

class CharacterPublish(View):
    def get(self, request, *args, **kwargs):
        if kwargs['type'] == 'monster':
            obj = get_object_or_404(models.Monster, pk=kwargs['pk'])
            form = forms.MonsterPublishForm()
        elif kwargs['type'] == 'npc':
            obj = get_object_or_404(models.NPC, pk=kwargs['pk'])
            form = forms.NPCPublishForm()
        elif kwargs['type'] == 'player':
            obj = get_object_or_404(models.Player, pk=kwargs['pk'])
            form = forms.PlayerPublishForm()

        if obj.user == request.user:
            if obj.is_published == True:
                return redirect('tavern:tavern_character_detail',
                    type=kwargs['type'], pk=kwargs['pk'])
            return render(self.request, 'characters/character_publish.html', {
                'obj': obj,
                'form': form,
                'type': kwargs['type'],
            })
        raise Http404

    def post(self, request, *args, **kwargs):
        if kwargs['type'] == 'monster':
            obj = get_object_or_404(models.Monster, pk=kwargs['pk'])
            form = forms.MonsterPublishForm(request.POST, instance=obj)
        elif kwargs['type'] == 'npc':
            obj = get_object_or_404(models.NPC, pk=kwargs['pk'])
            form = forms.NPCPublishForm(request.POST, instance=obj)
        elif kwargs['type'] == 'player':
            obj = get_object_or_404(models.Player, pk=kwargs['pk'])
            form = forms.PlayerPublishForm(request.POST, instance=obj)

        if obj.user == request.user:
            # publish to the tavern
            obj = form.save(commit=False)
            obj.is_published = True
            obj.published_date = timezone.now()
            obj.save()
            # redirect to the tavern page
            messages.success(request, 'Character published', fail_silently=True)
            return redirect('tavern:tavern_character_detail',
                type=kwargs['type'], pk=kwargs['pk'])
        raise Http404


class CharacterUnpublish(View):
    def get(self, request, *args, **kwargs):
        obj = get_character_object(kwargs['type'], kwargs['pk'])
        if obj.user == request.user:
            # remove from the tavern
            obj.is_published = False
            obj.save()

            # delete the importers
            obj.importers.clear()

            messages.success(request, 'Character unpublished', fail_silently=True)

            if kwargs['type'] == 'monster':
                # delete the reviews
                Review.objects.filter(monster=obj).delete()
                return redirect('characters:monster_detail', monster_pk=obj.pk)
            elif kwargs['type'] == 'npc':
                # delete the reviews
                Review.objects.filter(npc=obj).delete()
                return redirect('characters:npc_detail', npc_pk=obj.pk)
            elif kwargs['type'] == 'player':
                # delete the reviews
                Review.objects.filter(player=obj).delete()
                return redirect('characters:player_detail', player_pk=obj.pk)
        raise Http404
