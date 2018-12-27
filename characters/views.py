from itertools import chain
from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from . import forms
from . import models
from campaign.models import Campaign
from characters.utils import create_character_copy, get_character_stats, get_character_types
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

            if character_type == "Other":
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
                return render(request, 'characters/ch_y.html', {
                    'characters': characters,
                    'character': character,
                    'character_types': character_types,
                    'stats': get_character_stats(character),
                })
            raise Http404
        else:
            return render(request, 'characters/ch_n.html')
        raise Http404

@login_required
def character_create(request):
    # form for character name and notes
    form = forms.CharacterForm()
    # formset for character attributes
    formset = forms.AttributeFormSet()
    # preset attributes for attribute name dropdown
    suggested_attributes = character_suggested_attributes.attrs
    # sort the attributes alphabetically
    suggested_attributes.sort()

    if request.method == 'POST':
        form = forms.CharacterForm(request.POST)
        formset = forms.AttributeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            character = form.save(commit=False)
            # set the character's user
            character.user = request.user
            character.save()

            attributes = formset.save(commit=False)
            for attribute in attributes:
                # assign the attribute to the character
                attribute.character = character
                attribute.save()

            messages.add_message(request, messages.SUCCESS, "Character created")
            return redirect(character.get_absolute_url())

    return render(request, 'characters/character_form.html', {
        'assets': at_tagging(request),
        'form': form,
        'formset': formset,
        'suggested_attributes': suggested_attributes,
    })

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

    return render(request, 'characters/character_form.html', {
        'assets': at_tagging(request),
        'suggested_attributes': character_suggested_attributes.attrs,
        'form': form,
        'formset': formset,
        'character': character,
    })

class CharacterPublish(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(models.GeneralCharacter, pk=kwargs['pk'])
        form = forms.CharacterPublishForm()
        if character.user == request.user:
            if character.is_published == True:
                return redirect('tavern:tavern_character_detail', pk=kwargs['pk'])
            return render(self.request, 'characters/character_publish.html', {
                'character': character,
                'form': form,
            })
        raise Http404

    def post(self, request, *args, **kwargs):
        character = get_object_or_404(models.GeneralCharacter, pk=kwargs['pk'])
        form = forms.CharacterPublishForm(request.POST, instance=character)
        if character.user == request.user:
            # publish to the tavern
            character = form.save(commit=False)
            character.is_published = True
            character.published_date = timezone.now()
            character.save()
            # redirect to the tavern page
            messages.success(request, 'Character published', fail_silently=True)
            return redirect('tavern:tavern_character_detail', pk=kwargs['pk'])
        raise Http404

class CharacterUnpublish(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(models.GeneralCharacter, pk=kwargs['pk'])
        if character.user == request.user:
            # remove from the tavern
            character.is_published = False
            character.save()

            # delete the importers
            character.importers.clear()

            messages.success(request, 'Character unpublished', fail_silently=True)

            # delete the reviews
            Review.objects.filter(character=character).delete()
            return redirect('characters:character_detail', pk=character.pk)
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

