from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models
from characters import models as character_models

import json


@login_required
def campaign_detail(request, campaign_pk=None, chapter_pk=None, section_pk=None):
    if campaign_pk:
        this_campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        if this_campaign.user == request.user:
            chapters = sorted(models.Chapter.objects.filter(campaign=this_campaign),
            key=lambda chapter: chapter.order)

            if chapter_pk:
                this_chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
            else:
                if len(chapters) > 0:
                    this_chapter = chapters[0]
                else:
                    this_chapter = None

            sections = []
            for chapter in chapters:
                sections.append(sorted(
                    models.Section.objects.filter(chapter=chapter),
                    key=lambda section: section.order
                    ))
            sections = [item for sublist in sections for item in sublist]

            if section_pk:
                this_section = get_object_or_404(models.Section, pk=section_pk)
            else:
                this_section = None

            if this_chapter:
                if this_section:
                    return render(request, 'campaign/campaign_detail.html', {'this_campaign': this_campaign, 'this_chapter': this_chapter, 'this_section': this_section, 'chapters': chapters, 'sections': sections})
                else:
                    return render(request, 'campaign/campaign_detail.html', {'this_campaign': this_campaign, 'this_chapter': this_chapter, 'chapters': chapters, 'sections': sections})
            else:
                return render(request, 'campaign/campaign_detail.html', {'this_campaign': this_campaign})
        else:
            raise Http404
    else:
        this_campaign = None
        user = None
        if request.user.is_authenticated():
            user = request.user.pk
        campaigns = sorted(models.Campaign.objects.filter(user=user),
            key=lambda campaign: campaign.title)
        if len(campaigns) > 0:
            this_campaign = campaigns[0]

            chapters = sorted(models.Chapter.objects.filter(campaign=this_campaign), key=lambda chapter: chapter.order)
            if len(chapters) > 0:
                this_chapter = chapters[0]
            else:
                this_chapter = None

            sections = []
            for chapter in chapters:
                sections.append(sorted(
                    models.Section.objects.filter(chapter=chapter),
                    key=lambda section: section.order
                    ))
            sections = [item for sublist in sections for item in sublist]

            return render(request, 'campaign/campaign_detail.html', {'this_campaign': this_campaign, 'this_chapter': this_chapter, 'chapters': chapters, 'sections': sections})
        return render(request, 'campaign/campaign_detail.html', {'this_campaign': this_campaign})


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
    return render(request, 'campaign/chapter_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': campaign})

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
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': campaign, 'chapter': chapter})


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
    return render(request, 'campaign/chapter_form.html', {'form': form, 'formset': section_forms, 'monsters': monsters, 'npcs': npcs, 'campaign': chapter.campaign, 'chapter': chapter, 'sections': sections})

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

        form = forms.SectionForm(instance=section)
        if request.method == 'POST':
            form = forms.SectionForm(instance=section, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated section: {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(section.get_absolute_url())
    else:
        raise Http404
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': section.chapter.campaign, 'chapter': section.chapter, 'section': section})

@login_required
def campaign_print(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        chapters = sorted(models.Chapter.objects.filter(campaign=campaign),
            key=lambda chapter: chapter.order
            )
        sections = sorted(models.Section.objects.filter(campaign=campaign),
            key=lambda section: section.order
            )
        monsters = sorted(character_models.Monster.objects.filter(user=request.user),
            key=lambda monster: monster.name.lower()
            )
        npcs = sorted(character_models.NPC.objects.filter(user=request.user),
            key=lambda npc: npc.name.lower()
            ) 
        return render(request, 'campaign/campaign_print.html', {'campaign': campaign, 'chapters': chapters, 'sections': sections, 'monsters': monsters, 'npcs': npcs})
    else:
        raise Http404
    

@login_required
def campaign_delete(request, campaign_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        form = forms.DeleteCampaignForm(instance=campaign)
        if request.method == 'POST':
            form = forms.DeleteCampaignForm(request.POST, instance=campaign)
            if campaign.user.pk == request.user.pk:
                campaign.delete()
                messages.add_message(request, messages.SUCCESS, "Campaign deleted!")
                return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404
    return render(request, 'campaign/campaign_delete.html', {'form': form, 'campaign': campaign})


@login_required
def chapter_delete(request, campaign_pk, chapter_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        form = forms.DeleteChapterForm(instance=chapter)
        if request.method == 'POST':
            form = forms.DeleteChapterForm(request.POST, instance=chapter)
            if chapter.user.pk == request.user.pk:
                chapter.delete()
                messages.add_message(request, messages.SUCCESS, "Chapter deleted!")
                return HttpResponseRedirect(reverse('campaign:campaign_detail', kwargs={'campaign_pk': campaign.pk}))
    else:
        raise Http404
    return render(request, 'campaign/chapter_delete.html', {'form': form, 'chapter': chapter})

@login_required
def section_delete(request, campaign_pk, chapter_pk, section_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
    if campaign.user == request.user:
        chapter = get_object_or_404(models.Chapter, pk=chapter_pk)
        section = get_object_or_404(models.Section, pk=section_pk)
        form = forms.DeleteSectionForm(instance=section)
        if request.method == 'POST':
            form = forms.DeleteSectionForm(request.POST, instance=section)
            if section.user.pk == request.user.pk:
                section.delete()
                messages.add_message(request, messages.SUCCESS, "Section deleted!")
                return HttpResponseRedirect(reverse('campaign:campaign_detail', kwargs={'campaign_pk': campaign.pk, 'chapter_pk': chapter.pk}))
    else:
        raise Http404
    return render(request, 'campaign/section_delete.html', {'form': form, 'section': section})

@login_required
def campaign_import(request):
    user_import = None
    form = forms.ImportCampaignForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return HttpResponse("no user_import to get")
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
            return HttpResponseRedirect(campaign.get_absolute_url())
    return render(request, 'campaign/campaign_import.html', {'form': form, 'user_import': user_import})

@login_required
def campaign_export(request, campaign_pk):
    if campaign_pk:
        campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
        chapters = sorted(models.Chapter.objects.filter(campaign=campaign),
            key=lambda chapter: chapter.order
            )
        sections = sorted(models.Section.objects.filter(campaign=campaign),
            key=lambda section: section.order
            )
        monsters = sorted(character_models.Monster.objects.filter(user=request.user),
            key=lambda monster: monster.name.lower()
            )
        npcs = sorted(character_models.NPC.objects.filter(user=request.user),
            key=lambda npc: npc.name.lower()
            )
        return render(request, 'campaign/campaign_export.html', {'campaign': campaign, 'chapters': chapters, 'sections': sections, 'monsters': monsters, 'npcs': npcs})
    else:
        raise Http404