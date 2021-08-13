from bs4 import BeautifulSoup
from collections import OrderedDict
from itertools import chain
from shutil import copyfile
import json
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from . import forms
from . import models
from . import utils
from characters.models import Monster, NPC, Player
from dungeonomics.utils import at_tagging, rating_monster
from dungeonomics import settings
from items.models import Item
from locations.models import Location, World
from posts.models import Post
from tables.models import Table, TableOption
from tavern.models import Review


class CreateTemplate(LoginRequiredMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the objects to be used in mentions.
        context['data'] = at_tagging(self.request)

        # Check if we have a campaign PK.
        if 'campaign_pk' in self.kwargs:
            context['campaign'] = models.Campaign.objects.get(
                user=self.request.user,
                pk=self.kwargs['campaign_pk'],
            )
            # Set the QoL next order value.
            context['next_order'] = utils.get_next_order(context['campaign'])

        # Check if we have a chapter PK.
        if 'chapter_pk' in self.kwargs:
            context['chapter'] = models.Chapter.objects.get(
                pk=self.kwargs['chapter_pk'],
            )
            # Set the QoL next order value.
            context['next_order'] = utils.get_next_order(context['chapter'])

        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)

        # Send the request object to the form.
        kwargs['request'] = self.request

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)

            # Set the object's user.
            self.object.user = request.user

            # Set the campaign if we're creating anything other than a new campaign.
            if not self.model == models.Campaign:
                self.object.campaign = self.get_context_data()['campaign']

            # Set the chapter if we're creating a new section.
            if self.model == models.Section:
                self.object.chapter = self.get_context_data()['chapter']

            return self.form_valid(form)

        else:
            return self.form_invalid(form)

class CampaignCreate(CreateTemplate):
    model = models.Campaign
    form_class = forms.CampaignForm

class ChapterCreate(CreateTemplate):
    model = models.Chapter
    form_class = forms.ChapterForm

class SectionCreate(CreateTemplate):
    model = models.Section
    form_class = forms.SectionForm

class UpdateTemplate(LoginRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the objects to be used in mentions.
        context['data'] = at_tagging(self.request)

        # Check if we have a campaign PK.
        if 'campaign_pk' in self.kwargs:
            context['campaign'] = models.Campaign.objects.get(
                user=self.request.user,
                pk=self.kwargs['campaign_pk'],
            )
            # Set the QoL next order value.
            context['next_order'] = utils.get_next_order(context['campaign'])

        # Check if we have a chapter PK.
        if 'chapter_pk' in self.kwargs:
            context['chapter'] = models.Chapter.objects.get(
                pk=self.kwargs['chapter_pk'],
            )
            # Set the QoL next order value.
            context['next_order'] = utils.get_next_order(context['chapter'])

        # Check if we have a section PK.
        if 'section_pk' in self.kwargs:
            context['section'] = models.Section.objects.get(
                pk=self.kwargs['section_pk'],
            )

        # Set the formset based on which model we're updating.
        if 'chapter_pk' in self.kwargs:
            context['formset'] = forms.SectionInlineFormSet(
                queryset=context['chapter'].section_set.all(),
            )
        elif 'campaign_pk' in self.kwargs:
            context['formset'] = forms.ChapterInlineFormSet(
                queryset=context['campaign'].chapter_set.all(),
            )

        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)

        # Send the request object to the form.
        kwargs['request'] = self.request

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        # Set the formset based on which model we're updating.
        formset = None
        if self.model == models.Chapter:
            formset = forms.SectionInlineFormSet(
                request.POST,
                queryset=self.object.section_set.all(),
            )
        elif self.model == models.Campaign:
            formset = forms.ChapterInlineFormSet(
                request.POST,
                queryset=self.object.chapter_set.all(),
            )

        if form.is_valid():
            if formset:
                if formset.is_valid():
                    self.objects = formset.save(commit=False)

                    for object in self.objects:

                        # Set the object's user.
                        object.user = request.user

                        # Set the campaign if we're updating anything other than a campaign.
                        if not self.model == models.Campaign:
                            object.campaign = self.get_context_data()['campaign']

                        # Set the chapter if we're updating a section.
                        if self.model == models.Section:
                            object.chapter = self.get_context_data()['chapter']

                        object.save()

                    for object in formset.deleted_objects:
                        object.delete()

                else:
                    return self.form_invalid(formset)

            return self.form_valid(form)

        else:
            return self.form_invalid(form)

class CampaignUpdate(UpdateTemplate):
    model = models.Campaign
    form_class = forms.CampaignForm
    pk_url_kwarg = 'campaign_pk'

class ChapterUpdate(UpdateTemplate):
    model = models.Chapter
    form_class = forms.ChapterForm
    pk_url_kwarg = 'chapter_pk'

class SectionUpdate(UpdateTemplate):
    model = models.Section
    form_class = forms.SectionForm
    pk_url_kwarg = 'section_pk'

class CampaignDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'campaign_pk' in kwargs:
            campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])

            # Check if this campaign belongs to the user requesting it.
            if campaign.user != request.user:
                return

            # Get the campaign's party posts.
            posts = campaign.post_set.all().order_by('-date')[:5]

            if 'chapter_pk' in kwargs:
                # Get the requested chapter.
                chapter = get_object_or_404(models.Chapter, pk=kwargs['chapter_pk'])
            else:
                # If no chapter was specified, get the first chapter in the campaign.
                chapters = campaign.chapter_set.all()
                if chapters:
                    chapter = chapters.first()
                else:
                    # This campaign has no chapters.
                    chapter = None

            if 'section_pk' in kwargs:
                # Get the requested section.
                section = get_object_or_404(models.Section, pk=kwargs['section_pk'])
            else:
                section = None

            # Set the content toolbar.
            if section:
                content = (section, section.section_toolbar)
            elif chapter:
                content = (chapter, chapter.chapter_toolbar)
            elif campaign:
                content = (campaign, campaign.campaign_toolbar)
            else:
                content = (None, None)
        else:
            return redirect('campaign:campaign_create')

        return render(request, 'campaign/campaign_detail.html', {
            'campaign': campaign,
            'content': content,
            'posts': posts,
        })

    def post(self, request, *args, **kwargs):
        pass

@login_required
def campaign_print(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if campaign.user == request.user:
            chapters = sorted(models.Chapter.objects.filter(campaign=campaign), key=lambda chapter: chapter.order)
            sections = sorted(models.Section.objects.filter(campaign=campaign), key=lambda section: section.order)
            monsters = sorted(Monster.objects.filter(user=request.user), key=lambda monster: monster.name.lower())
            npcs = sorted(NPC.objects.filter(user=request.user), key=lambda npc: npc.name.lower())
            items = sorted(Item.objects.filter(user=request.user), key=lambda item: item.name.lower())
            worlds = sorted(World.objects.filter(user=request.user), key=lambda world: world.name.lower())
            return render(request, 'campaign/campaign_print.html', {
                'campaign': campaign,
                'chapters': chapters,
                'sections': sections,
                'monsters': monsters,
                'npcs': npcs,
                'items': items,
                'worlds': worlds,
            })
        else:
            raise Http404
    else:
        raise Http404

@login_required
def campaign_delete(request, campaign_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        campaign.delete()
        messages.success(request, 'Campaign deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404

@login_required
def chapter_delete(request, campaign_pk, chapter_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        if chapter.user == request.user:
            chapter.delete()
            messages.success(request, 'Chapter deleted', fail_silently=True)
            return HttpResponseRedirect(reverse('campaign:campaign_detail', kwargs={'campaign_pk': campaign.pk}))
    else:
        raise Http404

@login_required
def section_delete(request, campaign_pk, chapter_pk, section_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        section = get_object_or_404(models.Section, pk=section_pk)
        if section.user == request.user:
            section.delete()
            messages.success(request, 'Section deleted', fail_silently=True)
            return HttpResponseRedirect(reverse('campaign:campaign_detail', kwargs={
                'campaign_pk': campaign.pk,
                'chapter_pk': chapter.pk,
            }))
    else:
        raise Http404


class CampaignExport(View):
    def get(self, request, *args, **kwargs):
        if kwargs['campaign_pk']:
            campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
            if campaign.user == request.user:
                json_export = utils.campaign_export(campaign)
                return render(request, 'campaign/campaign_export.html', {
                    'campaign': campaign,
                    'campaign_items': json_export,
                })
        raise Http404


class CampaignImport(View):
    def get(self, request, *args, **kwargs):
        form = forms.ImportCampaignForm()
        return render(request, 'campaign/campaign_import.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ImportCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            if request.POST.get('user_import'):
                json_export = request.POST.get('user_import')
                utils.campaign_import(request.user, campaign, json_export)
                return HttpResponseRedirect(campaign.get_absolute_url())
        return Http404


class CampaignParty(View):
    def get(self, request, campaign_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if utils.has_campaign_access(request.user, campaign_pk):
            posts = Post.objects.filter(campaign=campaign).order_by('-date')[:10]
            return render(self.request, 'campaign/campaign_party.html', {
                'campaign': campaign,
                'posts': posts,
            })
        else:
            raise Http404


class CampaignPartyInvite(View):
    def get(self, request, campaign_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if request.user == campaign.user:
            return render(self.request, 'campaign/campaign_party_invite.html', {'campaign': campaign})
        else:
            raise Http404


class CampaignPartyInviteAccept(View):
    def get(self, request, campaign_public_url):
        campaign = get_object_or_404(models.Campaign, public_url=campaign_public_url)
        players = Player.objects.filter(user=request.user)
        return render(self.request, 'campaign/campaign_party_invite_accept.html', {
            'campaign': campaign,
            'players': players,
        })

    def post(self, request, campaign_public_url):
        campaign = get_object_or_404(models.Campaign, public_url=campaign_public_url)
        player_pk = self.request.POST.get('player')
        player = get_object_or_404(Player, pk=player_pk)
        if player.user == request.user:
            player.campaigns.add(campaign)
            return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404


class CampaignPartyRemove(View):
    def get(self, request, campaign_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if request.user == campaign.user:
            return render(self.request, 'campaign/campaign_party_remove.html', {'campaign': campaign})
        else:
            raise Http404

    def post(self, request, campaign_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if campaign.user == request.user:
            players = self.request.POST.getlist('players')
            # for each player, remove them from the campaign
            for pk in players:
                player = get_object_or_404(Player, pk=pk)
                player.campaigns.remove(campaign)
            return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404

class CampaignPartyPlayersDetail(View):
    def get(self, request, campaign_pk, player_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if utils.has_campaign_access(request.user, campaign_pk):
            player = get_object_or_404(Player, pk=player_pk)
            return render(self.request, 'campaign/campaign_party_player_detail.html', {
                'campaign': campaign,
                'player': player,
            })
        else:
            raise Http404


class CampaignPublish(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            form = forms.CampaignPublishForm()
            return render(self.request, 'campaign/campaign_publish.html', {
                'campaign': campaign,
                'form': form,
            })
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            form = forms.CampaignPublishForm(request.POST, instance=campaign)
            # publish to the tavern
            campaign = form.save(commit=False)
            campaign.is_published = True
            campaign.published_date = timezone.now()
            campaign.save()
            # redirect to the tavern page
            messages.success(request, 'Campaign published', fail_silently=True)
            return redirect('tavern:tavern_campaign_detail', campaign_pk=campaign.pk)
        else:
            raise Http404


class CampaignUnpublish(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            # remove from the tavern
            campaign.is_published = False
            campaign.save()

            # delete the reviews
            Review.objects.filter(campaign=campaign).delete()

            # delete the importers
            campaign.importers.clear()

            messages.success(request, 'Campaign unpublished', fail_silently=True)
            return redirect('campaign:campaign_detail', campaign_pk=campaign.pk)
        else:
            raise Http404
