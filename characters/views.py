from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models


@login_required
def monster_detail(request, monster_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    monsters = sorted(models.Monster.objects.filter(user=user),
        key=lambda monster: monster.name.lower()
        )
    if monster_pk:
        this_monster = get_object_or_404(models.Monster, pk=monster_pk)
        if this_monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})
        else:
            raise Http404
    elif len(monsters) > 0:
        this_monster = monsters[0]
        if this_monster.user == request.user:
            return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})
        else:
            raise Http404
    else:
        this_monster = None
    return render(request, 'characters/monster_detail.html', {'this_monster': this_monster, 'monsters': monsters})

@login_required
def npc_detail(request, npc_pk=''):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    npcs = sorted(models.NPC.objects.filter(user=user),
        key=lambda npc: npc.name.lower()
        )
    if npc_pk:
        this_npc = get_object_or_404(models.NPC, pk=npc_pk)
        if this_npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})
        else:
            raise Http404
    elif len(npcs) > 0:
        this_npc = npcs[0]
        if this_npc.user == request.user:
            return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})
        else:
            raise Http404
    else:
        this_npc = None
    return render(request, 'characters/npc_detail.html', {'this_npc': this_npc, 'npcs': npcs})

@login_required
def player_detail(request, player_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    players = sorted(models.Player.objects.filter(user=user),
        key=lambda player: player.player_name.lower()
        )
    if player_pk:
        this_player = get_object_or_404(models.Player, pk=player_pk)
        if this_player.user == request.user:
            return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})
        else:
            raise Http404
    elif len(players) > 0:
        this_player = players[0]
        if this_player.user == request.user:
            return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})
        else:
            raise Http404
    else:
        this_player = None
    return render(request, 'characters/player_detail.html', {'this_player': this_player, 'players': players})


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
def player_create(request):
    form = forms.PlayerForm()
    if request.method == 'POST':
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.add_message(request, messages.SUCCESS, "Player created!")
            return HttpResponseRedirect(player.get_absolute_url())
    return render(request, 'characters/player_form.html', {'form': form})

@login_required
def monster_update(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.MonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.MonsterForm(instance=monster, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated monster: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(monster.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/monster_form.html', {'form': form, 'monster': monster})

@login_required
def npc_update(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.NPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.NPCForm(instance=npc, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated NPC: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(npc.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/npc_form.html', {'form': form, 'npc': npc})

@login_required
def player_update(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.PlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.PlayerForm(instance=player, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated player: {}".format(form.cleaned_data['character_name']))
                return HttpResponseRedirect(player.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/player_form.html', {'form': form, 'player': player})


class MonsterDelete(LoginRequiredMixin, DeleteView):
    model = models.Monster
    success_url = reverse_lazy('characters:monster_detail')
    slug_field = "pk"
    slug_url_kwarg = "monster_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Monster deleted!")
        return super(MonsterDelete, self).delete(request, *args, **kwargs)


@login_required
def monster_delete(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.DeleteMonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.DeleteMonsterForm(request.POST, instance=monster)
            if monster.user.pk == request.user.pk:
                monster.delete()
                messages.add_message(request, messages.SUCCESS, "Monster deleted!")
                return HttpResponseRedirect(reverse('characters:monster_detail'))
    else:
        raise Http404
    return render(request, 'characters/monster_delete.html', {'form': form, 'monster': monster})

@login_required
def npc_delete(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.DeleteNPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.DeleteNPCForm(request.POST, instance=npc)
            if npc.user.pk == request.user.pk:
                npc.delete()
                messages.add_message(request, messages.SUCCESS, "NPC deleted!")
                return HttpResponseRedirect(reverse('characters:npc_detail'))
    else:
        raise Http404
    return render(request, 'characters/npc_delete.html', {'form': form, 'npc': npc})

class NPCDelete(LoginRequiredMixin, DeleteView):
    model = models.NPC
    success_url = reverse_lazy('characters:npc_detail')
    slug_field = "pk"
    slug_url_kwarg = "npc_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "NPC deleted!")
        return super(NPCDelete, self).delete(request, *args, **kwargs)

@login_required
def player_delete(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.DeletePlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.DeletePlayerForm(request.POST, instance=player)
            if player.user.pk == request.user.pk:
                player.delete()
                messages.add_message(request, messages.SUCCESS, "Player deleted!")
                return HttpResponseRedirect(reverse('characters:player_detail'))
    else:
        raise Http404
    return render(request, 'characters/player_delete.html', {'form': form, 'player': player})

class PlayerDelete(LoginRequiredMixin, DeleteView):
    model = models.Player
    success_url = reverse_lazy('characters:player_detail')
    slug_field = "pk"
    slug_url_kwarg = "player_pk"

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Player deleted!")
        return super(PlayerDelete, self).delete(request, *args, **kwargs)

@login_required
def monster_copy(request, monster_pk):
    monster = get_object_or_404(models.Monster, pk=monster_pk)
    if monster.user == request.user:
        form = forms.CopyMonsterForm(instance=monster)
        if request.method == 'POST':
            form = forms.CopyMonsterForm(request.POST, instance=monster)
            if monster.user.pk == request.user.pk:
                monster.pk = None
                monster.name = monster.name + "_Copy"
                monster.save()
                messages.add_message(request, messages.SUCCESS, "Monster Copied!")
                return HttpResponseRedirect(reverse('characters:monster_detail'))
    else:
        raise Http404
    return render(request, 'characters/monster_copy.html', {'form': form, 'monster': monster})


@login_required
def NPC_copy(request, npc_pk):
    npc = get_object_or_404(models.NPC, pk=npc_pk)
    if npc.user == request.user:
        form = forms.CopyNPCForm(instance=npc)
        if request.method == 'POST':
            form = forms.CopyNPCForm(request.POST, instance=npc)
            if npc.user.pk == request.user.pk:
                npc.pk = None
                npc.name = npc.name + "_Copy"
                npc.save()
                messages.add_message(request, messages.SUCCESS, "NPC Copied!")
                return HttpResponseRedirect(reverse('characters:npc_detail'))
    else:
        raise Http404
    return render(request, 'characters/npc_copy.html', {'form': form, 'npc': npc})


@login_required
def player_copy(request, player_pk):
    player = get_object_or_404(models.Player, pk=player_pk)
    if player.user == request.user:
        form = forms.CopyPlayerForm(instance=player)
        if request.method == 'POST':
            form = forms.CopyPlayerForm(request.POST, instance=player)
            if player.user.pk == request.user.pk:
                player.pk = None
                player.player_name = player.player_name + "_Copy"
                player.save()
                messages.add_message(request, messages.SUCCESS, "Player Copied!")
                return HttpResponseRedirect(reverse('characters:player_detail'))
    else:
        raise Http404
    return render(request, 'characters/player_copy.html', {'form': form, 'player': player})

