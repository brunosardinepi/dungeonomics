from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from . import forms
from . import models

from characters.models import Monster, NPC, Player
from items.models import Item
from locations.models import Location, World


@login_required
def table_detail(request, table_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    tables = sorted(
        models.Table.objects.filter(user=user),
        key=lambda table: table.name.lower()
    )
    if table_pk:
        table = get_object_or_404(models.Table, pk=table_pk)
        if table.user == request.user:
            return render(request,
                'tables/table_detail.html',
                {'table': table, 'tables': tables}
            )
        else:
            raise Http404
    elif len(tables) > 0:
        table = tables[0]
        if table.user == request.user:
            return render(request,
                'tables/table_detail.html',
                {'table': table, 'tables': tables}
            )
        else:
            raise Http404
    else:
        table = None
    return render(request,
        'tables/table_detail.html',
        {'table': table, 'tables': tables}
    )

@login_required
def table_create(request):
    monsters_raw = Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    worlds_raw = World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    form = forms.TableForm()
    formset = forms.TableOptionFormSet()
    if request.method == 'POST':
        form = forms.TableForm(request.POST)
        formset = forms.TableOptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            table = form.save(commit=False)
            table.user = request.user
            table.save()

            options = formset.save(commit=False)
            for option in options:
                option.table = table
                option.save()

            messages.add_message(request, messages.SUCCESS, "Table created!")
            return HttpResponseRedirect(table.get_absolute_url())


###
#        if request.method == 'POST':
#            form = forms.CampaignForm(request.POST, instance=campaign)
#            chapter_forms = forms.ChapterInlineFormSet(request.POST, queryset=form.instance.chapter_set.all())
#            if form.is_valid() and chapter_forms.is_valid():
#                form.save()
#                chapters = chapter_forms.save(commit=False)
#                for chapter in chapters:
#                    chapter.campaign = campaign
#                    chapter.user = request.user
#                    chapter.save()
#                for chapter in chapter_forms.deleted_objects:
#                    chapter.delete()
#                messages.add_message(request, messages.SUCCESS, "Updated campaign: {}".format(form.cleaned_data['title']))
#                return HttpResponseRedirect(campaign.get_absolute_url())
#            else:
#                print(form.errors)
#                print(chapter_forms.errors)
###







    return render(request, 'tables/table_form.html', {
        'form': form,
        'formset': formset,
        'monsters': monsters,
        'npcs': npcs,
        'items': items,
        'players': players,
        'worlds': worlds,
        'locations': locations,
    })

@login_required
def table_update(request, table_pk):
    monsters_raw = Monster.objects.filter(user=request.user).order_by('name')
    monsters = {}
    for monster in monsters_raw:
        monsters[monster.pk] = monster.name
    npcs_raw = NPC.objects.filter(user=request.user).order_by('name')
    npcs = {}
    for npc in npcs_raw:
        npcs[npc.pk] = npc.name
    items_raw = Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    players_raw = Player.objects.filter(user=request.user).order_by('player_name')
    players = {}
    for player in players_raw:
        players[player.pk] = player.player_name
    worlds_raw = World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    table = get_object_or_404(models.Table, pk=table_pk)
    if table.user == request.user:
        form = forms.TableForm(instance=table)
        if request.method == 'POST':
            form = forms.TableForm(instance=table, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request,
                    messages.SUCCESS,
                    "Updated table: {}".format(form.cleaned_data['name'])
                )
                return HttpResponseRedirect(table.get_absolute_url())
    else:
        raise Http404
    return render(request, 'tables/table_form.html', {
        'form': form,
        'table': table,
        'monsters': monsters,
        'npcs': npcs,
        'items': items,
        'players': players,
        'worlds': worlds,
        'locations': locations,
    })

@login_required
def table_delete(request, table_pk):
    table = get_object_or_404(models.Table, pk=table_pk)
    if table.user == request.user:
        table.delete()
        messages.success(request, 'Table deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('tables:table_detail'))
    else:
        raise Http404