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
from . import models

from characters.models import Monster, NPC, Player
from dungeonomics.utils import at_tagging
from items.models import Item
from locations.models import Location, World


@login_required
def table_detail(request, table_pk=None):
    user = None
    if request.user.is_authenticated:
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
    data = at_tagging(request)
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
    data['form'] = form
    data['formset'] = formset
    return render(request, 'tables/table_form.html', data)

@login_required
def table_update(request, table_pk):
    data = at_tagging(request)
    table = get_object_or_404(models.Table, pk=table_pk)
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
    data['form'] = form
    data['formset'] = formset
    data['table'] = table
    return render(request, 'tables/table_form.html', data)

@login_required
def table_delete(request, table_pk):
    table = get_object_or_404(models.Table, pk=table_pk)
    if table.user == request.user:
        table.delete()
        messages.success(request, 'Table deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('tables:table_detail'))
    else:
        raise Http404

@login_required
def table_roll(request):
    # get the table based on the pk ajax sends here
    table_pk = request.GET.get('pk', None)
    table = get_object_or_404(models.Table, pk=table_pk)

    # get the table options and put them into a list
    table_options = list(table.options())

    # pick a random one and return the pk
    random_option = choice(table_options).pk
    data = {
        'pk': random_option
    }

    return JsonResponse(data)

class TablesDelete(View):
    def get(self, request, *args, **kwargs):
        tables = models.Table.objects.filter(user=request.user).order_by('name')
        return render(request, 'tables/tables_delete.html', {'tables': tables})

    def post(self, request, *args, **kwargs):
        for table_pk in request.POST.getlist('table'):
            models.Table.objects.get(pk=table_pk).delete()
        return HttpResponseRedirect(reverse('tables:table_detail'))
