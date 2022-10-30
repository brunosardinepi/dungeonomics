from bs4 import BeautifulSoup
from campaign.models import Campaign, Chapter, Section
from campaign.utils import get_content_url, get_url_object
from characters.models import Monster, NPC, Player
from characters.utils import get_character_object
from django.apps import apps
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from dungeonomics.utils import at_tagging, rating_monster
from dungeonomics import settings
from items.models import Item
from itertools import chain
from locations.models import Location, World
from posts.models import Post
from tables.models import Table, TableOption
from tavern.utils import rating_stars_html
from tavern import forms, models
import uuid


class TavernView(View):
    def get(self, request, *args, **kwargs):
        models = [
            {'campaign': 'campaign'},
            {'characters': 'monster'},
            {'characters': 'npc'},
            {'characters': 'player'},
        ]
        objects = []
        for model in models:
            for app_label, model_name in model.items():
                # Get the object.
                model = apps.get_model(
                    app_label=app_label,
                    model_name=model_name,
                )
                for obj in model.objects.filter(is_published=True):
                    objects.append(obj)
        return render(self.request, 'tavern/tavern.html', {'objects': objects})

class TavernCampaignDetailView(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, public_url=kwargs['uuid'])
        if campaign.is_published == True:
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

            characters = {}
            for mention in campaign.mentions:
                if mention.__class__.__name__ not in characters:
                    characters[mention.__class__.__name__] = []
                if mention not in characters[mention.__class__.__name__]:
                    characters[mention.__class__.__name__].append(mention)

            return render(self.request, 'tavern/tavern_campaign_detail.html', {
                'campaign': campaign,
                'characters': characters,
                'reviews': reviews,
                'rating': rating,
                'importers': importers,
            })

class TavernCampaignReview(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, public_url=kwargs['uuid'])
        try:
            review = models.Review.objects.get(user=request.user, campaign=campaign)
        except models.Review.DoesNotExist:
            review = None
        if review:
            messages.info(
                request,
                "You've already submitted a review for this Campaign",
                fail_silently=True,
            )
            return redirect(campaign.get_tavern_url())
        else:
            form = forms.TavernReviewForm()
            return render(self.request, 'tavern/tavern_campaign_review.html', {
                'campaign': campaign,
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        campaign = get_object_or_404(Campaign, public_url=kwargs['uuid'])
        form = forms.TavernReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.campaign = campaign
            review.save()
            messages.success(request, 'Review submitted', fail_silently=True)
            return redirect(campaign.get_tavern_url())
        else:
            return render(self.request, 'tavern/tavern_campaign_review.html', {
                'campaign': campaign,
                'form': form,
            })

class TavernCharacterDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = get_character_object(kwargs['type'], kwargs['pk'])

        if obj.is_published == True:
            if kwargs['type'] == 'monster':
                reviews = models.Review.objects.filter(monster=obj).order_by('-date')
            elif kwargs['type'] == 'npc':
                reviews = models.Review.objects.filter(npc=obj).order_by('-date')
            elif kwargs['type'] == 'player':
                reviews = models.Review.objects.filter(player=obj).order_by('-date')

            rating = 0
            for review in reviews:
                rating += review.score
            if rating != 0:
                rating /= reviews.count()
            else:
                rating = 0
            rating = rating_stars_html(rating)

            importers = obj.importers.all().count()

            return render(self.request, 'tavern/tavern_character_detail.html', {
                'obj': obj,
                'type': kwargs['type'],
                'reviews': reviews,
                'rating': rating,
                'importers': importers,
            })
        else:
            raise Http404


class TavernCharacterImport(View):
    def get(self, request, *args, **kwargs):
        obj = get_character_object(kwargs['type'], kwargs['pk'])

        # create a copy of the obj
        obj.pk = None
        obj.id = None
        obj.user = request.user
        obj.is_published = False
        obj.save()

        # set this user as having imported the character
        # redirect to the imported character
        messages.success(request, "Character imported", fail_silently=True)
        if kwargs['type'] == 'monster':
            old_obj = get_object_or_404(Monster, pk=kwargs['pk'])
            old_obj.importers.add(request.user)
            return redirect('characters:monster_detail', monster_pk=obj.pk)
        elif kwargs['type'] == 'npc':
            old_obj = get_object_or_404(NPC, pk=kwargs['pk'])
            old_obj.importers.add(request.user)
            return redirect('characters:npc_detail', npc_pk=obj.pk)
        elif kwargs['type'] == 'player':
            old_obj = get_object_or_404(Player, pk=kwargs['pk'])
            old_obj.importers.add(request.user)
            # blank out the player name
            obj.player_name = ''
            obj.save()
            return redirect('characters:player_detail', player_pk=obj.pk)


class TavernCharacterReview(View):
    def get(self, request, *args, **kwargs):
        obj = get_character_object(kwargs['type'], kwargs['pk'])

        try:
            if kwargs['type'] == 'monster':
                review = models.Review.objects.get(user=request.user, monster=obj)
            elif kwargs['type'] == 'npc':
                review = models.Review.objects.get(user=request.user, npc=obj)
            elif kwargs['type'] == 'player':
                review = models.Review.objects.get(user=request.user, player=obj)
        except models.Review.DoesNotExist:
            review = None

        if review:
            messages.info(
                request,
                "You've already submitted a review for this character",
                fail_silently=True,
            )
            return redirect(
                'tavern:tavern_character_detail',
                type=kwargs['type'],
                pk=kwargs['pk'],
            )
        else:
            form = forms.TavernReviewForm()
            return render(self.request, 'tavern/tavern_character_review.html', {
                'obj': obj,
                'type': kwargs['type'],
                'form': form,
            })

    def post(self, request, *args, **kwargs):
        obj = get_character_object(kwargs['type'], kwargs['pk'])
        form = forms.TavernReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            if kwargs['type'] == 'monster':
                review.monster = obj
            elif kwargs['type'] == 'npc':
                review.npc = obj
            elif kwargs['type'] == 'player':
                review.player = obj
            review.save()
            messages.success(request, 'Review submitted', fail_silently=True)
            return redirect(
                'tavern:tavern_character_detail',
                type=kwargs['type'],
                pk=kwargs['pk'],
            )
        else:
            return render(self.request, 'tavern/tavern_character_review.html', {
                'obj': obj,
                'type': kwargs['type'],
            })

class TavernSearch(View):
    def get(self, request, *args, **kwargs):
        type = kwargs['type']
        if type == "campaign":
            results = Campaign.objects.filter(is_published=True).order_by('title')
        elif type == "monster":
            results = Monster.objects.filter(is_published=True).order_by('name')
        elif type == "npc":
            results = NPC.objects.filter(is_published=True).order_by('name')
        elif type == "player":
            results = Player.objects.filter(is_published=True).order_by('character_name')
        else:
            raise Http404
        return render(request, 'tavern/tavern_search.html', {
            'results': results,
            'type': type,
        })
