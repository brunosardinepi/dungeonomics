from itertools import chain
from collections import OrderedDict

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

from . import forms
from . import models
from campaign.models import Campaign
from characters.utils import (create_character_copy,
                              get_character_object,
                              get_character_types)
from dungeonomics.utils import at_tagging
from dungeonomics import character_suggested_attributes
from items import models as item_models
from locations import models as location_models
from tavern.models import Review
from tavern.utils import rating_stars_html

import json


class CharacterDetail(View):
    def get(self, request, *args, **kwargs):
        character_types = get_character_types(request.user)
        characters = OrderedDict()
        for character_type in character_types:
            # create a dict key for the type and an empty list to hold the characters
            # with the corresponding character type
            characters[character_type] = []

            if character_type == "None":
                # find all the characters for this user
                # that don't have an attribute named "Character type"
                characters_queryset = models.GeneralCharacter.objects.filter(
                    user=request.user).exclude(attribute__name="Character type")
                for character in characters_queryset:
                    characters[character_type].append(character)
            else:
                # find all the attributes that are named "Character type"
                # then get their associated character and add it to the dict list
                attributes = models.Attribute.objects.filter(
                    character__user=request.user,
                    name="Character type",
                    value=character_type,
                ).order_by('character__name')
                for attribute in attributes:
                    if attribute.character not in characters[character_type]:
                        characters[character_type].append(attribute.character)

        # check if we have a specific character to show
        try:
            character = models.GeneralCharacter.objects.get(pk=kwargs['pk'])
        # no character was specified
        except KeyError:
            # if the user has characters, show the first available
            if characters:
                first_character_type = next(iter(characters))
                character = characters[first_character_type][0]
            else:
                character = None

        if character:
            if character.user == request.user:
                stats = OrderedDict([
                    ("Strength", {"title": "STR", "attribute": None}),
                    ("Dexterity", {"title": "DEX", "attribute": None}),
                    ("Constitution", {"title": "CON", "attribute": None}),
                    ("Intelligence", {"title": "INT", "attribute": None}),
                    ("Wisdom", {"title": "WIS", "attribute": None}),
                    ("Charisma", {"title": "CHA", "attribute": None}),
                ])
                for stat, attribute in stats.items():
                    try:
                        attribute = character.attribute_set.get(name=stat)
                    except models.Attribute.DoesNotExist:
                        attribute = None
                    stats[stat]['attribute'] = attribute
                return render(request, 'characters/character_detail.html', {
                    'characters': characters,
                    'character': character,
                    'stats': stats,
                    'character_types': character_types,
                })
            raise Http404
        else:
            return render(request, 'characters/character_detail.html')
        raise Http404

class CharacterCreate(View):
    def get(self, request, *args, **kwargs):
        data = at_tagging(request)
        data['form'] = forms.CharacterForm()
        data['formset'] = forms.AttributeFormSet()
        data['suggested_attributes'] = character_suggested_attributes.attrs
        data['suggested_attributes'].sort()
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

class CharacterDelete(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(models.GeneralCharacter, pk=kwargs['pk'])
        if character.user == request.user:
            character.delete()
            messages.success(request, 'Character deleted', fail_silently=True)
            return redirect('characters:character_detail')
        raise Http404

class CharacterCopy(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(models.GeneralCharacter, pk=kwargs['pk'])
        if character.user == request.user:
            create_character_copy(character, request.user)
            character.name += "_copy"
            character.save()
            messages.add_message(request, messages.SUCCESS, "Character copied!")
            return redirect(character.get_absolute_url())
        raise Http404

@login_required
def character_srd(request):
    characters = sorted(models.GeneralCharacter.objects.filter(user=3029),
        key=lambda c: c.name.lower()
        )
    if request.method == 'POST':
        for pk in request.POST.getlist('character'):
            character = models.GeneralCharacter.objects.get(pk=pk)
            create_character_copy(character, request.user)
        return redirect('characters:character_detail')
    return render(request, 'characters/character_srd_form.html', {'characters': characters})

class CharactersDelete(View):
    def get(self, request, *args, **kwargs):
        characters = models.GeneralCharacter.objects.filter(
            user=request.user).order_by('name')
        return render(request, 'characters/characters_delete.html', {
            'characters': characters,
        })

    def post(self, request, *args, **kwargs):
        for character_pk in request.POST.getlist('character'):
            models.GeneralCharacter.objects.get(pk=character_pk).delete()
        return redirect('characters:character_detail')

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

