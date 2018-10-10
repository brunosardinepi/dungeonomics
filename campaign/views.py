from bs4 import BeautifulSoup
from itertools import chain
import json
from shutil import copyfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
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
from dungeonomics.utils import at_tagging
from dungeonomics import settings
from items.models import Item
from locations.models import Location, World
from posts.models import Post
from tables.models import Table, TableOption


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
        if request.user.is_authenticated:
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
            added_other = []
            added_worlds = []
            added_locations = []
            added_tables = []

            for item in combined_list:

                soup = BeautifulSoup(item.content, 'html.parser')

                for link in soup.find_all('a'):
                    url = utils.get_content_url(link)

                    obj = utils.get_url_object(url)

                    if obj:

                        # if World, get all the child locations
                        # if Location, get the World and all child locations
                        if isinstance(obj, World):
                            if obj.pk not in added_worlds:
                                # get all of the Locations that belong to this World
                                locations = Location.objects.filter(world=obj)

                                # add all of the new locations to lists for tracking
                                for location in locations:
                                    additional_assets.append(location)
                                    added_locations.append(location.pk)

                                # add the World to a list for tracking
                                additional_assets.append(obj)
                                added_worlds.append(obj.pk)

                        elif isinstance(obj, Location):
                            if obj.pk not in added_locations:
                                # add the location to our list
                                additional_assets.append(obj)
                                added_locations.append(obj.pk)

                                # get this Location's World
                                world = World.objects.get(pk=obj.world.pk)

                                if world.pk not in added_worlds:
                                    # append it to our list
                                    additional_assets.append(world)

                                    # get the World's Locations, excluding the Location we already have
                                    locations = Location.objects.filter(world=world).exclude(pk=obj.pk)

                                    # add all of the new locations to the list
                                    for location in locations:
                                        additional_assets.append(location)
                                        added_locations.append(location.pk)

                        elif isinstance(obj, Table):
                            if obj.pk not in added_tables:
                                # get all of the Table Options that belong to this Table
                                table_options = TableOption.objects.filter(table=obj)

                                # add all of the new Table Options to a list for tracking
                                for table_option in table_options:
                                    additional_assets.append(table_option)

                                # add the Table to a list for tracking
                                additional_assets.append(obj)
                                added_tables.append(obj.pk)

                        else:
                            if obj.pk not in added_other:
                                additional_assets.append(obj)
                                added_other.append(obj.pk)

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
                    "Table",
                    "TableOption",
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
                    "tables": {},
                    "tableoptions": {},
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

                    if isinstance(other, World) or isinstance(other, Location):
                        if other.image:

                            # create a new filename
                            random_string = create_random_string()
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

                    if isinstance(other, Monster):
                        asset_references['monsters'][old_pk] = new_pk
                    elif isinstance(other, NPC):
                        asset_references['npcs'][old_pk] = new_pk
                    elif isinstance(other, Item):
                        asset_references['items'][old_pk] = new_pk
                    elif isinstance(other, World):
                        asset_references['worlds'][old_pk] = new_pk
                    elif isinstance(other, Location):
                        asset_references['locations'][old_pk] = new_pk
                    elif isinstance(other, Table):
                        asset_references['tables'][old_pk] = new_pk
                    elif isinstance(other, TableOption):
                        asset_references['tableoptions'][old_pk] = new_pk

                # update any content with new pks
                # must be done after asset_references is populated
                for other in others:
                    # everything has 'content' except TableOption
                    if not isinstance(other, TableOption):
                        utils.replace_content_urls(other, asset_references)

                for old_pk, new_pk in asset_references['tableoptions'].items():
                    # for each tableoption, set the table to the newly created table
                    old_tableoption = TableOption.objects.get(pk=old_pk)
                    new_tableoption = TableOption.objects.get(pk=new_pk)
                    old_table = old_tableoption.table
                    new_table = Table.objects.get(pk=asset_references['tables'][old_table.pk])
                    new_tableoption.table = new_table
                    new_tableoption.save()

                for old_pk, new_pk in asset_references['locations'].items():
                    # for each location, set the parent location to the new parent location.
                    # also, set the world to the new world
                    old_location = Location.objects.get(pk=old_pk)
                    if old_location.parent_location:
                        old_location_parent = old_location.parent_location

                    new_location = Location.objects.get(pk=new_pk)
                    if new_location.parent_location:
                        new_location_parent = Location.objects.get(pk=asset_references['locations'][old_location_parent.pk])
                        new_location.parent_location = new_location_parent

                    old_world = old_location.world
                    new_world = World.objects.get(pk=asset_references['worlds'][old_world.pk])
                    new_location.world = new_world
                    new_location.save()

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


class TavernView(View):
    def get(self, request, *args, **kwargs):
        popular_campaigns = models.Campaign.objects.filter(is_published=True)
        recent_campaigns = models.Campaign.objects.filter(
            is_published=True).order_by('-published_date')
        return render(self.request, 'campaign/tavern.html', {
            'popular_campaigns': popular_campaigns,
            'recent_campaigns': recent_campaigns,
        })


class TavernDetailView(View):
    def get(self, request, *args, **kwargs):
        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
        if campaign.is_published == True:
            chapters = models.Chapter.objects.filter(campaign=campaign)
            sections = models.Section.objects.filter(campaign=campaign)

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

            monsters = []
            npcs = []
            items = []
            worlds = []
            locations = []
            tables = []

            for item in combined_list:
                soup = BeautifulSoup(item.content, 'html.parser')
                for link in soup.find_all('a'):
                    url = utils.get_content_url(link)
                    obj = utils.get_url_object(url)
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

            return render(self.request, 'campaign/tavern_detail.html', {
                'campaign': campaign,
                'chapters': chapters,
                'sections': sections,
                'monsters': monsters,
                'npcs': npcs,
                'items': items,
                'worlds': worlds,
                'locations': locations,
                'tables': tables,
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
            return redirect('tavern_detail', campaign_pk=campaign.pk)
        else:
            raise Http404