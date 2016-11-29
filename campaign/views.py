from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models
from characters import models as character_models


def campaign_list(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    campaigns = sorted(models.Campaign.objects.filter(user=user),
        key=lambda campaign: campaign.name
        )
    return render(request, 'campaign/campaign_list.html', {'campaigns': campaigns})

def campaign_detail(request, campaign_pk=None, chapter_pk=None, section_pk=None):
    if campaign_pk:
        this_campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
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
        this_campaign = None
        user = None
        if request.user.is_authenticated():
            user = request.user.pk
        campaigns = sorted(models.Campaign.objects.filter(user=user),
            key=lambda campaign: campaign.title)
        if len(campaigns) > 0:
            this_campaign = campaigns[0]
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
    return render(request, 'campaign/chapter_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': campaign})

@login_required
def section_create(request, campaign_pk, chapter_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
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
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': campaign, 'chapter': chapter})


@login_required
def campaign_update(request, campaign_pk):
    campaign = get_object_or_404(models.Campaign, pk=campaign_pk)
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
    return render(request, 'campaign/campaign_form.html', {'form': form, 'formset': chapter_forms, 'campaign': campaign})

@login_required
def chapter_update(request, campaign_pk, chapter_pk):
    chapter = get_object_or_404(models.Chapter, pk=chapter_pk, campaign_id=campaign_pk)
    monsters_raw = character_models.Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = character_models.NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name

    form = forms.ChapterForm(instance=chapter)
    if request.method == 'POST':
        form = forms.ChapterForm(instance=chapter, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated chapter: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(chapter.get_absolute_url())
    return render(request, 'campaign/chapter_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': chapter.campaign, 'chapter': chapter})

@login_required
def section_update(request, campaign_pk, chapter_pk, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk, chapter_id=chapter_pk, campaign_id=campaign_pk)
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
    return render(request, 'campaign/section_form.html', {'form': form, 'monsters': monsters, 'npcs': npcs, 'campaign': section.chapter.campaign, 'chapter': section.chapter, 'section': section})


class CampaignDelete(LoginRequiredMixin, DeleteView):
    model = models.Campaign
    success_url = reverse_lazy('home')
    slug_field = "pk"
    slug_url_kwarg = "campaign_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Campaign deleted!")
        return super(CampaignDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        campaign = super(CampaignDelete, self).get_object()
        if not campaign.user == self.request.user:
            raise Http404
        else:
            return campaign


class ChapterDelete(LoginRequiredMixin, DeleteView):
    model = models.Chapter
    success_url = reverse_lazy('home')
    slug_field = "pk"
    slug_url_kwarg = "chapter_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Chapter deleted!")
        return super(ChapterDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        chapter = super(ChapterDelete, self).get_object()
        if not chapter.user == self.request.user:
            raise Http404
        else:
            return chapter


class SectionDelete(LoginRequiredMixin, DeleteView):
    model = models.Section
    success_url = reverse_lazy('home')
    slug_field = "pk"
    slug_url_kwarg = "section_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Section deleted!")
        return super(SectionDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        section = super(SectionDelete, self).get_object()
        if not section.user == self.request.user:
            raise Http404
        else:
            return section