from bs4 import BeautifulSoup
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
from dungeonomics.utils import at_tagging, campaign_context, rating_monster
from dungeonomics import settings
from items.models import Item
from locations.models import Location, World
from posts.models import Post
from tables.models import Table, TableOption
from tavern.models import Review


@login_required
def campaign_detail(request, campaign_pk=None):
    data = campaign_context(
        request=request,
        data={},
        campaign_pk=campaign_pk,
        chapter_pk=None,
        section_pk=None,
    )
    data['action'] = "campaign_detail"
    return render(request, 'campaign/body_detail.html', data)

@login_required
def chapter_detail(request, campaign_pk, chapter_pk):
    data = campaign_context(
        request=request,
        data={},
        campaign_pk=campaign_pk,
        chapter_pk=chapter_pk,
        section_pk=None,
    )
    data['action'] = "chapter_detail"
    return render(request, 'campaign/body_detail.html', data)

@login_required
def section_detail(request, campaign_pk, chapter_pk, section_pk):
    data = campaign_context(
        request=request,
        data={},
        campaign_pk=campaign_pk,
        chapter_pk=chapter_pk,
        section_pk=section_pk,
    )
    data['action'] = "section_detail"
    return render(request, 'campaign/body_detail.html', data)

class CampaignCreate(LoginRequiredMixin, CreateView):
    model = models.Campaign
    fields = [
        'title',
    ]

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.user = self.request.user
        campaign.save()
        return HttpResponseRedirect(campaign.get_absolute_url())


class ChapterCreate(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            data = at_tagging(request)
            data = campaign_context(
                request=request,
                data=data,
                campaign_pk=kwargs['campaign_pk'],
                chapter_pk=None,
                section_pk=None,
            )
            data['action'] = "chapter_create"
            data['form'] = forms.ChapterForm()
            data['order_number'] = utils.get_next_order(data['campaign'])
            return render(request, 'campaign/cs_form.html', data)
        raise Http404

    def post(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            form = forms.ChapterForm(request.POST)
            if form.is_valid():
                chapter = form.save(commit=False)
                chapter.user = request.user
                chapter.campaign = campaign
                chapter.save()
                messages.add_message(request, messages.SUCCESS, "Chapter created")
                return HttpResponseRedirect(chapter.get_absolute_url())
        raise Http404


class SectionCreate(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            data = at_tagging(request)
            data = campaign_context(
                request=request,
                data=data,
                campaign_pk=kwargs['campaign_pk'],
                chapter_pk=kwargs['chapter_pk'],
                section_pk=None,
            )
            data['action'] = "section_create"
            data['form'] = forms.SectionForm()
            data['order_number'] = utils.get_next_order(data['chapter'])
            return render(request, 'campaign/cs_form.html', data)
        raise Http404

    def post(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.user == request.user:
            form = forms.SectionForm(request.POST)
            if form.is_valid():
                section = form.save(commit=False)
                section.user = request.user
                section.campaign = campaign
                section.chapter = get_object_or_404(models.Chapter,
                    pk=kwargs['chapter_pk'])
                section.save()
                messages.add_message(request, messages.SUCCESS, "Section created")
                return HttpResponseRedirect(section.get_absolute_url())
        raise Http404


@login_required
def campaign_update(request, campaign_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        form = forms.CampaignForm(instance=campaign)
        chapter_forms = forms.ChapterInlineFormSet(queryset=form.instance.chapter_set.all())
        if request.method == 'POST':
            form = forms.CampaignForm(request.POST, instance=campaign)
            chapter_forms = forms.ChapterInlineFormSet(request.POST, queryset=form.instance.chapter_set.all())
            if form.is_valid() and chapter_forms.is_valid():
                form.save()
                chapters = chapter_forms.save(commit=False)
                for chapter in chapters:
                    chapter.campaign = campaign
                    chapter.user = request.user
                    chapter.save()
                for chapter in chapter_forms.deleted_objects:
                    chapter.delete()
                messages.add_message(request, messages.SUCCESS, "Updated campaign: {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(campaign.get_absolute_url())
            else:
                print(form.errors)
                print(chapter_forms.errors)
    else:
        raise Http404
    return render(request, 'campaign/campaign_form.html', {'form': form, 'formset': chapter_forms, 'campaign': campaign})

@login_required
def chapter_update(request, campaign_pk, chapter_pk):
    chapter = get_object_or_404(models.Chapter, pk=chapter_pk, campaign_id=campaign_pk)
    if chapter.user == request.user:
        data = at_tagging(request)
        data = campaign_context(
            request=request,
            data=data,
            campaign_pk=chapter.campaign.pk,
            chapter_pk=chapter.pk,
            section_pk=None,
        )
        data['action'] = "chapter_update"
        form = forms.ChapterForm(instance=chapter)
        section_forms = forms.SectionInlineFormSet(queryset=form.instance.section_set.all())
        if request.method == 'POST':
            form = forms.ChapterForm(request.POST, instance=chapter)
            section_forms = forms.SectionInlineFormSet(
                request.POST, queryset=form.instance.section_set.all())
            if form.is_valid() and section_forms.is_valid():
                form.save()
                sections = section_forms.save(commit=False)
                for section in sections:
                    section.chapter = chapter
                    section.user = request.user
                    section.save()
                for section in section_forms.deleted_objects:
                    section.delete()
                messages.add_message(request, messages.SUCCESS, "Updated chapter: {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(chapter.get_absolute_url())
    else:
        raise Http404
    data['form'] = form
    data['formset'] = section_forms
    return render(request, 'campaign/cs_form.html', data)

@login_required
def section_update(request, campaign_pk, chapter_pk, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk, chapter_id=chapter_pk, campaign_id=campaign_pk)
    if section.user == request.user:
        data = at_tagging(request)
        data = campaign_context(
            request=request,
            data=data,
            campaign_pk=section.chapter.campaign.pk,
            chapter_pk=section.chapter.pk,
            section_pk=section.pk,
        )
        data['action'] = "section_update"
        form = forms.SectionForm(instance=section)
        if request.method == 'POST':
            form = forms.SectionForm(instance=section, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated section: {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(section.get_absolute_url())
    else:
        raise Http404
    data['form'] = form
    return render(request, 'campaign/cs_form.html', data)

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
        return HttpResponseRedirect(reverse('campaign:campaign_detail'))
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
