from bs4 import BeautifulSoup
from itertools import chain
import json
from shutil import copyfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from . import forms
from . import models
from . import utils
from characters import models as character_models
from dungeonomics.utils import at_tagging
from dungeonomics import settings
from items import models as item_models
from locations import models as location_models
from posts.models import Post


@login_required
def campaign_detail(request, campaign_pk=None, chapter_pk=None, section_pk=None):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        posts = Post.objects.filter(campaign=campaign).order_by('-date')[:5]
        if campaign.user == request.user:
            chapters = sorted(models.Chapter.objects.filter(campaign=campaign),
            key=lambda chapter: chapter.order)

            if chapter_pk:
                chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
            else:
                if len(chapters) > 0:
                    chapter = chapters[0]
                else:
                    chapter = None

            sections = []
            for c in chapters:
                sections.append(sorted(
                    models.Section.objects.filter(chapter=c),
                    key=lambda section: section.order
                    ))
            sections = [item for sublist in sections for item in sublist]

            if section_pk:
                section = get_object_or_404(models.Section, pk=section_pk)
            else:
                section = None

            if chapter:
                if section:
                    return render(request, 'campaign/campaign_detail.html', {
                        'campaign': campaign,
                        'chapter': chapter,
                        'section': section,
                        'chapters': chapters,
                        'sections': sections,
                        'posts': posts,
                    })
                else:
                    return render(request, 'campaign/campaign_detail.html', {
                        'campaign': campaign,
                        'chapter': chapter,
                        'chapters': chapters,
                        'sections': sections,
                        'posts': posts,
                    })
            else:
                return render(request, 'campaign/campaign_detail.html', {
                    'campaign': campaign,
                    'posts': posts,
                })
        else:
            raise Http404
    else:
        campaign = None
        user = None
        if request.user.is_authenticated():
            user = request.user.pk
        campaigns = sorted(models.Campaign.objects.filter(user=user),
            key=lambda campaign: campaign.title)
        if len(campaigns) > 0:
            campaign = campaigns[0]
            posts = Post.objects.filter(campaign=campaign).order_by('-date')[:5]

            chapters = sorted(models.Chapter.objects.filter(campaign=campaign), key=lambda chapter: chapter.order)
            if len(chapters) > 0:
                chapter = chapters[0]
            else:
                chapter = None

            sections = []
            for c in chapters:
                sections.append(sorted(
                    models.Section.objects.filter(chapter=c),
                    key=lambda section: section.order
                    ))
            sections = [item for sublist in sections for item in sublist]

            return render(request, 'campaign/campaign_detail.html', {
                'campaign': campaign,
                'chapter': chapter,
                'chapters': chapters,
                'sections': sections,
                'posts': posts,
            })
        return render(request, 'campaign/campaign_detail.html', {
            'campaign': campaign,
        })


class CampaignCreate(LoginRequiredMixin, CreateView):
    model = models.Campaign
    fields = [
        'title',
    ]

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.user = self.request.user
        campaign.save()
        messages.add_message(self.request, messages.SUCCESS, "Campaign created!")
        return HttpResponseRedirect(campaign.get_absolute_url())


@login_required
def chapter_create(request, campaign_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        data = at_tagging(request)
        form = forms.ChapterForm()
        if request.method == 'POST':
            form = forms.ChapterForm(request.POST)
            if form.is_valid():
                chapter = form.save(commit=False)
                chapter.user = request.user
                chapter.campaign = campaign
                chapter.save()
                messages.add_message(request, messages.SUCCESS, "Chapter created!")
                return HttpResponseRedirect(chapter.get_absolute_url())
    else:
        raise Http404
    data['campaign'] = campaign
    data['form'] = form
    return render(request, 'campaign/chapter_form.html', data)

@login_required
def section_create(request, campaign_pk, chapter_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        data = at_tagging(request)
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        form = forms.SectionForm()
        if request.method == 'POST':
            form = forms.SectionForm(request.POST)
            if form.is_valid():
                section = form.save(commit=False)
                section.user = request.user
                section.campaign = campaign
                section.chapter = chapter
                section.save()
                messages.add_message(request, messages.SUCCESS, "Section created!")
                return HttpResponseRedirect(section.get_absolute_url())
    else:
        raise Http404
    data['campaign'] = campaign
    data['chapter'] = chapter
    data['form'] = form
    return render(request, 'campaign/section_form.html', data)

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
        sections = models.Section.objects.filter(chapter=chapter)
        form = forms.ChapterForm(instance=chapter)
        section_forms = forms.SectionInlineFormSet(queryset=form.instance.section_set.all())
        if request.method == 'POST':
            form = forms.ChapterForm(request.POST, instance=chapter)
            section_forms = forms.SectionInlineFormSet(request.POST, queryset=form.instance.section_set.all())
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
    data['campaign'] = chapter.campaign
    data['chapter'] = chapter
    data['sections'] = sections
    data['form'] = form
    data['formset'] = section_forms
    return render(request, 'campaign/chapter_form.html', data)

@login_required
def section_update(request, campaign_pk, chapter_pk, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk, chapter_id=chapter_pk, campaign_id=campaign_pk)
    if section.user == request.user:
        data = at_tagging(request)
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
    data['campaign'] = section.chapter.campaign
    data['chapter'] = section.chapter
    data['section'] = section
    return render(request, 'campaign/section_form.html', data)

@login_required
def campaign_print(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if campaign.user == request.user:
            chapters = sorted(models.Chapter.objects.filter(campaign=campaign), key=lambda chapter: chapter.order)
            sections = sorted(models.Section.objects.filter(campaign=campaign), key=lambda section: section.order)
            monsters = sorted(character_models.Monster.objects.filter(user=request.user), key=lambda monster: monster.name.lower())
            npcs = sorted(character_models.NPC.objects.filter(user=request.user), key=lambda npc: npc.name.lower())
            items = sorted(item_models.Item.objects.filter(user=request.user), key=lambda item: item.name.lower())
            worlds = sorted(location_models.World.objects.filter(user=request.user), key=lambda world: world.name.lower())
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

@login_required
def campaign_export(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if campaign.user == request.user:

            chapters_queryset = models.Chapter.objects.filter(campaign=campaign).order_by('order')
            sections_queryset = models.Section.objects.filter(campaign=campaign).order_by('order')
            combined_list = list(chain(chapters_queryset, sections_queryset))

            # go through each chapter and section
            # find all of the hyperlinks
            # look through the dungeonomics links
            # get the type (item, monster, npc, player)
            # pull a copy of that resource and add it to a list
            # at the end, combine the list with the campaign items list
            # then serialize it

            additional_assets = []

            for item in combined_list:

                soup = BeautifulSoup(item.content, 'html.parser')

                for link in soup.find_all('a'):
                    url = utils.get_content_url(link)

                    obj = utils.get_url_object(url)

                    if obj:
                        additional_assets.append(obj)

            combined_list = list(chain(combined_list, additional_assets))
            campaign_items = serializers.serialize("json", combined_list, indent=2)

            return render(request, 'campaign/campaign_export.html', {
                'campaign': campaign,
                'campaign_items': campaign_items,
            })
    raise Http404

@login_required
def campaign_import(request):
    user_import = None
    form = forms.ImportCampaignForm()
    if request.method == 'POST':
        form = forms.ImportCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()

            if request.POST.get('user_import'):
                user_import = request.POST.get('user_import')

                chapters, sections, others = ([] for i in range(3))
                model_types = [
                    "Monster",
                    "NPC",
                    "Item",
                    "World",
                    "Location",
                ]

                for obj in serializers.deserialize("json", user_import):
                    if isinstance(obj.object, models.Chapter):
                        chapters.append(obj.object)
                    elif isinstance(obj.object, models.Section):
                        sections.append(obj.object)
                    elif obj.object.__class__.__name__ in model_types:
                        others.append(obj.object)

                asset_references = {
                    "monsters": {},
                    "npcs": {},
                    "items": {},
                    "worlds": {},
                    "locations": {},
                }

                # for each "other" asset,
                # create a copy of the asset
                # and update a dictionary that holds a reference of the old pk and the new pk

                for other in others:
                    # grab the old pk for reference
                    old_pk = other.pk

                    # create a copy of the asset
                    other.pk = None
                    other.user = request.user

                    if isinstance(other, location_models.World) or isinstance(other, location_models.Location):
                        if other.image:
                            # create a new filename
                            random_string = location_models.create_random_string()
                            ext = other.image.url.split('.')[-1]
                            new_filename = "media/user/images/%s.%s" % (random_string, ext)

                            # copy the old file to a new file
                            # and save it to the new object
                            old_image_url = settings.MEDIA_ROOT + other.image.name
                            new_image_url = settings.MEDIA_ROOT + new_filename
                            copyfile(old_image_url, new_image_url)
                            other.image = new_filename

                    other.save()

                    new_pk = other.pk

                    if isinstance(other, character_models.Monster):
                        asset_references['monsters'][old_pk] = new_pk
                    elif isinstance(other, character_models.NPC):
                        asset_references['npcs'][old_pk] = new_pk
                    elif isinstance(other, item_models.Item):
                        asset_references['items'][old_pk] = new_pk
                    elif isinstance(other, location_models.World):
                        asset_references['worlds'][old_pk] = new_pk
                    elif isinstance(other, location_models.Location):
                        asset_references['locations'][old_pk] = new_pk

                print("asset_references = {}".format(asset_references))
#                for location in asset_references['locations']:
                for old_pk, new_pk in asset_references['locations'].items():
#                    print("location = {}".format(location))
                    print("old_pk = {}, new_pk = {}".format(old_pk, new_pk))
                    # for each location,
                    # set the parent location to the new parent location.
                    # if there isn't a parent location,
                    # set the world to the new world
                    old_location = location_models.Location.objects.get(pk=old_pk)
                    print("old_location = {} (pk = {})".format(old_location, old_location.pk))
                    if old_location.parent_location:
                        print("there is a parent location")
                        old_location_parent = old_location.parent_location
                        print("old_location_parent = {} (pk = {})".format(old_location_parent, old_location_parent.pk))

                    new_location = location_models.Location.objects.get(pk=new_pk)
                    print("new_location = {} (pk = {})".format(new_location, new_location.pk))
                    if new_location.parent_location:
                        print("new_location parent = {} (pk = {})".format(new_location.parent_location, new_location.parent_location.pk))
                        new_location_parent = location_models.Location.objects.get(pk=asset_references['locations'][old_location_parent.pk])
                        new_location.parent_location = new_location_parent
                        print("new_location_parent = {} (pk = {})".format(new_location_parent, new_location_parent.pk))
                    else:
                        print("there is no parent location")
                    ########### NEED TO GET ALL WORLD LOCATIONS FOR EACH LOCATION, AND ALL LOCATIONS FOR EACH WORLD
                    print("*" * 20)

                # go through each chapter and create a reference to its pk,
                # then create the copy of the chapter.
                # go through each section and find those that belong to the
                # old chapter, and create a copy of them going to the new
                # chapter.
                # update the campaign pk along the way.

                for chapter in chapters:

                    # create a reference to the chapter's original pk
                    old_pk = chapter.pk

                    # create a new copy of the chapter
                    chapter.pk = None
                    chapter.user = request.user
                    chapter.campaign = campaign
                    chapter.save()

                    utils.replace_content_urls(chapter, asset_references)

                    for section in sections:
                        # find sections that belong to the chapter
                        if section.chapter.pk == old_pk:

                            # create a new copy of the section
                            section.pk = None
                            section.user = request.user
                            section.chapter = chapter
                            section.campaign = campaign
                            section.save()

                            utils.replace_content_urls(section, asset_references)

                return HttpResponseRedirect(campaign.get_absolute_url())

        else:
            return Http404

    return render(request, 'campaign/campaign_import.html', {'form': form})

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
        players = character_models.Player.objects.filter(user=request.user)
        return render(self.request, 'campaign/campaign_party_invite_accept.html', {
            'campaign': campaign,
            'players': players,
        })

    def post(self, request, campaign_public_url):
        campaign = get_object_or_404(models.Campaign, public_url=campaign_public_url)
        player_pk = self.request.POST.get('player')
        player = get_object_or_404(character_models.Player, pk=player_pk)
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
                player = get_object_or_404(character_models.Player, pk=pk)
                player.campaigns.remove(campaign)
            return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404

class CampaignPartyPlayersDetail(View):
    def get(self, request, campaign_pk, player_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if utils.has_campaign_access(request.user, campaign_pk):
            player = get_object_or_404(character_models.Player, pk=player_pk)
            return render(self.request, 'campaign/campaign_party_player_detail.html', {
                'campaign': campaign,
                'player': player,
            })
        else:
            raise Http404