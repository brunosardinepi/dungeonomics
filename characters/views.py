from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models


def monster_detail(request, monster_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monster_pk:
        this_monster = get_object_or_404(models.Monster, pk=monster_pk)
    elif len(monsters) > 0:
        this_monster = monsters[0]
    else:
        this_monster = None
    return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})

def npc_detail(request, npc_pk=''):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npc_pk:
        this_npc = get_object_or_404(models.NPC, pk=npc_pk)
    elif len(npcs) > 0:
        this_npc = npcs[0]
    else:
        this_npc = None
    return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})


@login_required
def monster_create(request):
    form = forms.MonsterForm()
    if request.method == 'POST':
        form = forms.MonsterForm(request.POST)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.user = request.user
            monster.save()
            messages.add_message(request, messages.SUCCESS, "Monster created!")
            return HttpResponseRedirect(monster.get_absolute_url())
    return render(request, 'characters/monster_form.html', {'form': form})

@login_required
def npc_create(request):
    form = forms.NPCForm()
    if request.method == 'POST':
        form = forms.NPCForm(request.POST)
        if form.is_valid():
            npc = form.save(commit=False)
            npc.user = request.user
            npc.save()
            messages.add_message(request, messages.SUCCESS, "NPC created!")
            return HttpResponseRedirect(npc.get_absolute_url())
    return render(request, 'characters/npc_form.html', {'form': form})

@login_required
def monster_update(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    form = forms.MonsterForm(instance=monster)
    if request.method == 'POST':
        form = forms.MonsterForm(instance=monster, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated monster: {}".format(form.cleaned_data['name']))
            return HttpResponseRedirect(monster.get_absolute_url())
    return render(request, 'characters/monster_form.html', {'form': form, 'monster': monster})

@login_required
def npc_update(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    form = forms.NPCForm(instance=npc)
    if request.method == 'POST':
        form = forms.NPCForm(instance=npc, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Updated NPC: {}".format(form.cleaned_data['name']))
            return HttpResponseRedirect(npc.get_absolute_url())
    return render(request, 'characters/npc_form.html', {'form': form, 'npc': npc})


class MonsterDelete(LoginRequiredMixin, DeleteView):
    model = models.Monster
    success_url = reverse_lazy('characters:monster_detail')
    slug_field = "pk"
    slug_url_kwarg = "monster_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Monster deleted!")
        return super(MonsterDelete, self).delete(request, *args, **kwargs)


class NPCDelete(LoginRequiredMixin, DeleteView):
    model = models.NPC
    success_url = reverse_lazy('characters:npc_detail')
    slug_field = "pk"
    slug_url_kwarg = "npc_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "NPC deleted!")
        return super(NPCDelete, self).delete(request, *args, **kwargs)