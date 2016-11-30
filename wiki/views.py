from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy


def wiki_home(request, section_pk=None):
    if section_pk:
        this_section = get_object_or_404(models.Section, pk=section_pk)
        return render(request, 'wiki/wiki_home.html', {'this_section': this_section})
    else:
        sections = sorted(models.Section.objects.all(),
            key=lambda section: section.title)
        if len(sections) > 0:
            this_section = sections[0]
        return render(request, 'wiki/wiki_home.html', {'this_section': this_section})