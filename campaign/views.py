from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from . import forms
from . import models
from . import utils
from characters import models as character_models
from items import models as item_models
from locations import models as location_models
from posts.models import Post

import json


@login_required
def campaign_detail(request, campaign_pk=None, chapter_pk=None, section_pk=None):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        posts = Post.objects.filter(campaign=campaign).order_by('date')[:5]
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
            posts = Post.objects.filter(campaign=campaign).order_by('date')[:5]

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
        monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
        monsters = {}
        for monster in monsters_raw:
            monsters[monster.pk] = monster.name
        npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
        npcs = {}
        for npc in npcs_raw:
            npcs[npc.pk] = npc.name
        items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
        items = {}
        for item in items_raw:
            items[item.pk] = item.name
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
    return render(request, 'campaign/chapter_form.html', {
        'form': form,
        'monsters': monsters,
        'npcs': npcs,
        'items': items,
        'players': players,
        'campaign': campaign,
        'worlds': worlds,
        'locations': locations,
    })

@login_required
def section_create(request, campaign_pk, chapter_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
        monsters = {}
        for monster in monsters_raw:
            monsters[monster.pk] = monster.name
        npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
        npcs = {}
        for npc in npcs_raw:
            npcs[npc.pk] = npc.name
        items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
        items = {}
        for item in items_raw:
            items[item.pk] = item.name
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
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'campaign': campaign, 'chapter': chapter, 'worlds': worlds, 'locations': locations})


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
        sections = models.Section.objects.filter(chapter=chapter)
        monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
        monsters = {}
        for monster in monsters_raw:
            monsters[monster.pk] = monster.name
        npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
        npcs = {}
        for npc in npcs_raw:
            npcs[npc.pk] = npc.name
        items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
        items = {}
        for item in items_raw:
            items[item.pk] = item.name
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
    return render(request, 'campaign/chapter_form.html', {'form': form, 'formset': section_forms, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'campaign': chapter.campaign, 'chapter': chapter, 'sections': sections, 'worlds': worlds, 'locations': locations})

@login_required
def section_update(request, campaign_pk, chapter_pk, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk, chapter_id=chapter_pk, campaign_id=campaign_pk)
    if section.user == request.user:
        monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
        monsters = {}
        for monster in monsters_raw:
            monsters[monster.pk] = monster.name
        npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
        npcs = {}
        for npc in npcs_raw:
            npcs[npc.pk] = npc.name
        items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
        items = {}
        for item in items_raw:
            items[item.pk] = item.name
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

        form = forms.SectionForm(instance=section)
        if request.method == 'POST':
            form = forms.SectionForm(instance=section, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated section: {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(section.get_absolute_url())
    else:
        raise Http404
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'items': items, 'players': players, 'campaign': section.chapter.campaign, 'chapter': section.chapter, 'section': section, 'worlds': worlds, 'locations': locations})

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
            return render(request, 'campaign/campaign_print.html', {'campaign': campaign, 'chapters': chapters, 'sections': sections, 'monsters': monsters, 'npcs': npcs, 'items': items, 'worlds': worlds})
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
def campaign_import(request):
    user_import = None
    form = forms.ImportCampaignForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            for chapter_order, chapter_attributes in user_import["chapters"].items():
                new_chapter = models.Chapter(
                    title=chapter_attributes["title"],
                    user=request.user,
                    campaign=campaign,
                    order=chapter_order,
                    content=chapter_attributes["content"]
                    )
                new_chapter.save()
                if "sections" in chapter_attributes:
                    for section_order, section_attributes in chapter_attributes["sections"].items():
                        new_section = models.Section(
                            title=section_attributes["title"],
                            user=request.user,
                            campaign=campaign,
                            chapter=new_chapter,
                            order=section_order,
                            content=section_attributes["content"]
                            )
                        new_section.save()
            if "monsters" in user_import:
                for monster, monster_attributes in user_import["monsters"].items():
                    new_monster = character_models.Monster(
                        user=request.user,
                        name=monster,
                        alignment=monster_attributes["alignment"],
                        size=monster_attributes["size"],
                        languages=monster_attributes["languages"],
                        strength=monster_attributes["strength"],
                        dexterity=monster_attributes["dexterity"],
                        constitution=monster_attributes["constitution"],
                        intelligence=monster_attributes["intelligence"],
                        wisdom=monster_attributes["wisdom"],
                        charisma=monster_attributes["charisma"],
                        armor_class=monster_attributes["armor_class"],
                        hit_points=monster_attributes["hit_points"],
                        speed=monster_attributes["speed"],
                        saving_throws=monster_attributes["saving_throws"],
                        skills=monster_attributes["skills"],
                        creature_type=monster_attributes["creature_type"],
                        damage_vulnerabilities=monster_attributes["damage_vulnerabilities"],
                        damage_immunities=monster_attributes["damage_immunities"],
                        damage_resistances=monster_attributes["damage_resistances"],
                        condition_immunities=monster_attributes["condition_immunities"],
                        senses=monster_attributes["senses"],
                        challenge_rating=monster_attributes["challenge_rating"],
                        traits=monster_attributes["traits"],
                        actions=monster_attributes["actions"],
                        notes=monster_attributes["notes"]
                    )
                    new_monster.save()
            if "npcs" in user_import:
                for npc, npc_attributes in user_import["npcs"].items():
                    new_npc = character_models.NPC(
                        user=request.user,
                        name=npc,
                        alignment=npc_attributes["alignment"],
                        size=npc_attributes["size"],
                        languages=npc_attributes["languages"],
                        strength=npc_attributes["strength"],
                        dexterity=npc_attributes["dexterity"],
                        constitution=npc_attributes["constitution"],
                        intelligence=npc_attributes["intelligence"],
                        wisdom=npc_attributes["wisdom"],
                        charisma=npc_attributes["charisma"],
                        armor_class=npc_attributes["armor_class"],
                        hit_points=npc_attributes["hit_points"],
                        speed=npc_attributes["speed"],
                        saving_throws=npc_attributes["saving_throws"],
                        skills=npc_attributes["skills"],
                        npc_class=npc_attributes["npc_class"],
                        age=npc_attributes["age"],
                        height=npc_attributes["height"],
                        weight=npc_attributes["weight"],
                        creature_type=npc_attributes["creature_type"],
                        damage_vulnerabilities=npc_attributes["damage_vulnerabilities"],
                        damage_immunities=npc_attributes["damage_immunities"],
                        damage_resistances=npc_attributes["damage_resistances"],
                        condition_immunities=npc_attributes["condition_immunities"],
                        senses=npc_attributes["senses"],
                        challenge_rating=npc_attributes["challenge_rating"],
                        traits=npc_attributes["traits"],
                        actions=npc_attributes["actions"],
                        notes=npc_attributes["notes"]
                    )
                    new_npc.save()
            if "items" in user_import:
                for item, item_attributes in user_import["items"].items():
                    new_item = item_models.Item(
                        user=request.user,
                        name=item,
                        item_type=item_attributes["item_type"],
                        rarity=item_attributes["rarity"],
                        description=item_attributes["description"]
                    )
                    new_item.save()
            return HttpResponseRedirect(campaign.get_absolute_url())
    return render(request, 'campaign/campaign_import.html', {'form': form, 'user_import': user_import})

@login_required
def campaign_export(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if campaign.user == request.user:
            chapters = sorted(models.Chapter.objects.filter(campaign=campaign), key=lambda chapter: chapter.order)
            monsters = sorted(character_models.Monster.objects.filter(user=request.user), key=lambda monster: monster.name.lower())
            npcs = sorted(character_models.NPC.objects.filter(user=request.user), key=lambda npc: npc.name.lower())
            items = sorted(item_models.Item.objects.filter(user=request.user), key=lambda item: item.name.lower())
            for chapter in chapters:
                chapter.content = json.dumps(chapter.content)
            for monster in monsters:
                monster.traits = json.dumps(monster.traits)
                monster.actions = json.dumps(monster.actions)
                monster.notes = json.dumps(monster.notes)
            for npc in npcs:
                npc.traits = json.dumps(npc.traits)
                npc.actions = json.dumps(npc.actions)
                npc.notes = json.dumps(npc.notes)
            for item in items:
                item.description = json.dumps(item.description)
            return render(request, 'campaign/campaign_export.html', {'campaign': campaign, 'chapters': chapters, 'monsters': monsters, 'npcs': npcs, 'items': items})
        else:
            raise Http404
    else:
        raise Http404


class CampaignParty(View):
    def get(self, request, campaign_pk):
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if utils.has_campaign_access(request.user, campaign_pk):
            posts = Post.objects.filter(campaign=campaign).order_by('date')[:10]
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