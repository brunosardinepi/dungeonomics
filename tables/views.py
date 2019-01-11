from random import choice

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View

from . import forms
from .models import Table

from characters.models import Monster, NPC, Player
from dungeonomics.utils import at_tagging
from items.models import Item
from locations.models import Location, World


@login_required
def table_detail(request, pk=None):
    tables = Table.objects.filter(user=request.user).order_by('name')

    if pk:
        table = get_object_or_404(Table, pk=pk)
    elif len(tables) > 0:
        table = tables[0]
    else:
        table = None

    if table.user == request.user:
        return render(request, 'tables/table_y.html', {'table': table, 'tables': tables})
    raise Http404

@login_required
def table_create(request):
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
    return render(request, 'tables/table_form.html', {
        'assets': at_tagging(request),
        'form': form,
        'formset': formset,
    })

@login_required
def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if table.user == request.user:
        form = forms.TableForm(instance=table)
        formset = forms.TableOptionFormSet(instance=table)
        if request.method == 'POST':
            form = forms.TableForm(request.POST, instance=table)
            formset = forms.TableOptionFormSet(request.POST, instance=table)
            if form.is_valid() and formset.is_valid():
                form.save()
                options = formset.save(commit=False)
                for option in options:
                    option.table = table
                    option.save()
                for option in formset.deleted_objects:
                    option.delete()
                messages.add_message(request,
                    messages.SUCCESS,
                    "Updated table: {}".format(form.cleaned_data['name'])
                )
                return HttpResponseRedirect(table.get_absolute_url())
    else:
        raise Http404
    return render(request, 'tables/table_form.html', {
        'assets': at_tagging(request),
        'form': form,
        'formset': formset,
        'table': table,
    })

@login_required
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if table.user == request.user:
        table.delete()
        messages.success(request, 'Table deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('tables:table_detail'))
    else:
        raise Http404

@login_required
def table_roll(request):
    # get the table based on the pk ajax sends here
    pk = request.GET.get('pk', None)
    table = get_object_or_404(Table, pk=pk)

    # get the table options and put them into a list
    table_options = list(table.options())

    # pick a random one and return the pk
    random_option = choice(table_options).pk
    data = {'pk': random_option}

    return JsonResponse(data)

class TablesDelete(View):
    def get(self, request, *args, **kwargs):
        tables = Table.objects.filter(user=request.user).order_by('name')
        return render(request, 'tables/tables_delete.html', {'tables': tables})

    def post(self, request, *args, **kwargs):
        for pk in request.POST.getlist('table'):
            Table.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('tables:table_detail'))
