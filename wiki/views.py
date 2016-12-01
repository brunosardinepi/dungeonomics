from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from . import models
from . import forms


@login_required
def wiki_home(request, section_pk=None, subsection_pk=None):
    sections = sorted(models.Section.objects.all(),
        key=lambda section: section.title)

    subsections = []
    for section in sections:
        subsections.append(sorted(
            models.Subsection.objects.filter(section=section),
            key=lambda subsection: subsection.order
            ))
    subsections = [item for sublist in subsections for item in sublist]

    if section_pk:
        this_section = get_object_or_404(models.Section, pk=section_pk)
        this_subsections = sorted(models.Subsection.objects.filter(section=this_section),
        key=lambda subsection: subsection.order)
        if subsection_pk:
            this_subsection = get_object_or_404(models.Subsection, pk=subsection_pk)
        else:
            this_subsection = None

        if this_subsection:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'this_subsection': this_subsection, 'sections': sections, 'subsections': subsections})
        else:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})
    else:
        this_section = None
        sections = sorted(models.Section.objects.all(),
            key=lambda section: section.title)
        if len(sections) > 0:
            this_section = sections[0]
        return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})

@staff_member_required
def section_create(request):
    form = forms.SectionForm()
    if request.method == 'POST':
        form = forms.SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.save()
            messages.add_message(request, messages.SUCCESS, "Section created!")
            return HttpResponseRedirect(section.get_absolute_url())
    return render(request, 'wiki/section_form.html', {'form': form})

@staff_member_required
def subsection_create(request, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk)
    form = forms.SubsectionForm()
    if request.method == 'POST':
        form = forms.SubsectionForm(request.POST)
        if form.is_valid():
            subsection = form.save(commit=False)
            subsection.section = section
            subsection.save()
            messages.add_message(request, messages.SUCCESS, "Subsection created!")
            return HttpResponseRedirect(subsection.get_absolute_url())
    return render(request, 'wiki/subsection_form.html', {'form': form, 'section': section})

@staff_member_required
def section_update(request, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk)
    form = forms.SectionForm(instance=section)
    if request.method == 'POST':
        form = forms.SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated section: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(section.get_absolute_url())
    return render(request, 'wiki/section_form.html', {'form': form, 'section': section})

@staff_member_required
def subsection_update(request, section_pk, subsection_pk):
    subsection = get_object_or_404(models.Subsection, pk=subsection_pk, section_id=section_pk)
    form = forms.SubsectionForm(instance=subsection)
    if request.method == 'POST':
        form = forms.SubsectionForm(request.POST, instance=subsection)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated subsection: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(subsection.get_absolute_url())
    return render(request, 'wiki/subsection_form.html', {'form': form, 'section': subsection.section, 'subsection': subsection})


# class SectionDelete(PermissionRequiredMixin, DeleteView):
#     permission_required = 'user.is_staff'
#     model = models.Campaign
#     success_url = reverse_lazy('home')
#     slug_field = "pk"
#     slug_url_kwarg = "campaign_pk"

#     def delete(self, request, *args, **kwargs):
#         messages.add_message(self.request, messages.SUCCESS, "Campaign deleted!")
#         return super(CampaignDelete, self).delete(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         campaign = super(CampaignDelete, self).get_object()
#         if not campaign.user == self.request.user:
#             raise Http404
#         else:
#             return campaign

@staff_member_required
def section_delete(request, section_pk):
    section = get_object_or_404(models.Section, pk=section_pk)
    if request.user.is_staff and section:
        section.delete()
        messages.add_message(request, messages.SUCCESS, "Deleted section: {}".format(form.cleaned_data['title']))
        return HttpResponseRedirect('wiki:home')
    else:
        raise Http404
    # return render(request, 'wiki/section_confirm_delete.html', {'section': section})


# class ChapterDelete(LoginRequiredMixin, DeleteView):
#     model = models.Chapter
#     success_url = reverse_lazy('home')
#     slug_field = "pk"
#     slug_url_kwarg = "chapter_pk"

#     def delete(self, request, *args, **kwargs):
#         messages.add_message(self.request, messages.SUCCESS, "Chapter deleted!")
#         return super(ChapterDelete, self).delete(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         chapter = super(ChapterDelete, self).get_object()
#         if not chapter.user == self.request.user:
#             raise Http404
#         else:
#             return chapter

@staff_member_required
def subsection_delete(request, section_pk, subsection_pk):
    subsection = get_object_or_404(models.Subsection, pk=subsection_pk, section_id=section_pk)
    form = forms.SubsectionForm(instance=subsection)
    if request.method == 'POST':
        form = forms.SubsectionForm(request.POST, instance=subsection)
        if form.is_valid():
            subsection.delete()
            messages.add_message(request, messages.SUCCESS, "Deleted subsection: {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect('wiki:home')
    return render(request, 'wiki/subsection_confirm_delete.html', {'form': form, 'section': subsection.section, 'subsection': subsection})