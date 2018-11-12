from bs4 import BeautifulSoup
from itertools import chain
import uuid

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from . import forms
from . import models
from .utils import rating_stars_html
from campaign.models import Campaign, Chapter, Section
from campaign.utils import (campaign_export,
                            campaign_import,
                            get_content_url,
                            get_url_object)
from characters.models import GeneralCharacter
from characters.utils import get_character_stats
from dungeonomics.utils import at_tagging
from dungeonomics import settings
from items.models import Item
from locations.models import Location, World
from posts.models import Post
from tables.models import Table, TableOption


class TavernView(View):
    def get(self, request, *args, **kwargs):
        popular_campaigns = Campaign.objects.filter(is_published=True)
        popular_campaigns = sorted(
            popular_campaigns,
            key=lambda c: c.rating(),
            reverse=True)[:5]
        popular_characters = GeneralCharacter.objects.filter(is_published=True)
        popular_characters = sorted(
            popular_characters,
            key=lambda c: c.rating(),
            reverse=True)[:5]

        recent_campaigns = Campaign.objects.filter(
            is_published=True).order_by('-published_date')[:5]
        recent_characters = GeneralCharacter.objects.filter(
            is_published=True).order_by('-published_date')[:5]

        return render(self.request, 'tavern/tavern.html', {
            'popular_campaigns': popular_campaigns,
            'popular_characters': popular_characters,
            'recent_campaigns': recent_campaigns,
            'recent_characters': recent_characters,
        })

class TavernCampaignDetailView(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['pk'])
        if campaign.is_published == True:
            chapters = Chapter.objects.filter(campaign=campaign)
            sections = Section.objects.filter(campaign=campaign)

            chapters_queryset = Chapter.objects.filter(campaign=campaign).order_by('order')
            sections_queryset = Section.objects.filter(campaign=campaign).order_by('order')
            combined_list = list(chain(chapters_queryset, sections_queryset))

            # go through each chapter and section
            # find all of the hyperlinks
            # look through the dungeonomics links
            # get the type (item, monster, npc, player)
            # pull a copy of that resource and add it to a list
            # at the end, combine the list with the campaign items list
            # then serialize it

            monsters = []
            npcs = []
            items = []
            worlds = []
            locations = []
            tables = []

            for item in combined_list:
                soup = BeautifulSoup(item.content, 'html.parser')
                for link in soup.find_all('a'):
                    url = get_content_url(link)
                    obj = get_url_object(url)
                    if obj:
                        if isinstance(obj, Monster):
                            if obj not in monsters:
                                # add to a list for tracking
                                monsters.append(obj)
                        elif isinstance(obj, NPC):
                            if obj not in npcs:
                                npcs.append(obj)
                        elif isinstance(obj, Item):
                            if obj not in items:
                                items.append(obj)
                        elif isinstance(obj, World):
                            if obj not in worlds:
                                worlds.append(obj)
                        elif isinstance(obj, Location):
                            if obj not in locations:
                                locations.append(obj)
                        elif isinstance(obj, Table):
                            if obj not in tables:
                                tables.append(obj)

            reviews = models.Review.objects.filter(campaign=campaign).order_by('-date')
            rating = 0
            for review in reviews:
                rating += review.score
            if rating != 0:
                rating /= reviews.count()
            else:
                rating = 0
            rating = rating_stars_html(rating)

            importers = campaign.importers.all().count()

            return render(self.request, 'tavern/tavern_campaign_detail.html', {
                'campaign': campaign,
                'chapters': chapters,
                'sections': sections,
                'monsters': monsters,
                'npcs': npcs,
                'items': items,
                'worlds': worlds,
                'locations': locations,
                'tables': tables,
                'reviews': reviews,
                'rating': rating,
                'importers': importers,
            })
        else:
            raise Http404


class TavernCampaignReview(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['pk'])
        try:
            review = models.Review.objects.get(user=request.user, campaign=campaign)
        except models.Review.DoesNotExist:
            review = None
        if review:
            messages.info(request, "You've already submitted a review for this Campaign", fail_silently=True)
            return redirect('tavern:tavern_campaign_detail', pk=campaign.pk)
        else:
            form = forms.TavernReviewForm()
            return render(self.request, 'tavern/tavern_campaign_review.html', {
                'campaign': campaign,
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['pk'])
        form = forms.TavernReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.campaign = campaign
            review.save()
            messages.success(request, 'Review submitted', fail_silently=True)
            return redirect('tavern:tavern_campaign_detail', pk=campaign.pk)
        else:
            return render(self.request, 'tavern/tavern_campaign_review.html', {
                'campaign': campaign,
                'form': form,
            })


class TavernCampaignImport(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=kwargs['pk'])

        # get the campaign export
        json_export = campaign_export(campaign)

        # create a copy of the campaign
        campaign.pk = None
        campaign.id = None
        campaign.public_url = uuid.uuid4()
        campaign.user = request.user
        campaign.is_published = False
        campaign.save()

        # import to this user's account
        campaign_import(request.user, campaign, json_export)

        # set this user as having imported the campaign
        old_campaign = get_object_or_404(Campaign, pk=kwargs['pk'])
        old_campaign.importers.add(request.user)

        # redirect to the imported campaign
        messages.success(request, "Campaign imported", fail_silently=True)
        return redirect('campaign:campaign_detail', campaign_pk=campaign.pk)


class TavernCharacterDetailView(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(GeneralCharacter, pk=kwargs['pk'])

        if character.is_published == True:
            reviews = models.Review.objects.filter(character=character).order_by('-date')

            rating = 0
            for review in reviews:
                rating += review.score
            if rating != 0:
                rating /= reviews.count()
            else:
                rating = 0
            rating = rating_stars_html(rating)

            importers = character.importers.all().count()

            return render(self.request, 'tavern/tavern_character_detail.html', {
                'character': character,
                'stats': get_character_stats(character),
                'reviews': reviews,
                'rating': rating,
                'importers': importers,
            })
        else:
            raise Http404


class TavernCharacterImport(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(GeneralCharacter, pk=kwargs['pk'])

        # create a copy of the character
        character.pk = None
        character.id = None
        character.user = request.user
        character.is_published = False
        character.save()

        # set this user as having imported the character
        # redirect to the imported character
        messages.success(request, "Character imported", fail_silently=True)
        old_character = get_object_or_404(GeneralCharacter, pk=kwargs['pk'])
        old_character.importers.add(request.user)
        return redirect('characters:character_detail', pk=character.pk)

class TavernCharacterReview(View):
    def get(self, request, *args, **kwargs):
        character = get_object_or_404(GeneralCharacter, pk=kwargs['pk'])

        try:
            review = models.Review.objects.get(user=request.user, character=character)
        except models.Review.DoesNotExist:
            review = None

        if review:
            messages.info(
                request,
                "You've already submitted a review for this character",
                fail_silently=True,
            )
            return redirect('tavern:tavern_character_detail', pk=kwargs['pk'])
        else:
            form = forms.TavernReviewForm()
            return render(self.request, 'tavern/tavern_character_review.html', {
                'character': character,
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        character = get_object_or_404(GeneralCharacter, pk=kwargs['pk'])
        form = forms.TavernReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.character = character
            review.save()
            messages.success(request, 'Review submitted', fail_silently=True)
            return redirect(
                'tavern:tavern_character_detail',
                pk=kwargs['pk'],
            )
        else:
            return render(self.request, 'tavern/tavern_character_review.html', {
                'obj': obj,
            })

class TavernSearch(View):
    def get(self, request, *args, **kwargs):
        type = kwargs['type']
        if type == "campaigns":
            results = Campaign.objects.filter(is_published=True).order_by('title')
        elif type == "characters":
            results = GeneralCharacter.objects.filter(is_published=True).order_by('name')
        else:
            raise Http404
        return render(request, 'tavern/tavern_search.html', {
            'results': results,
            'type': type,
        })
