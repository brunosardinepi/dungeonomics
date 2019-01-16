from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from . import forms
from .models import Item
from .utils import create_item_copy

from characters import models as character_models
from dungeonomics.utils import at_tagging
from locations import models as location_models


@login_required
def item_detail(request, pk=None):
    items = Item.objects.filter(user=request.user).order_by('name')

    # select an active item to show
    if pk:
        item = get_object_or_404(Item, pk=pk)
    elif len(items) > 0:
        item = items[0]
    else:
        item = None
        return render(request, 'items/item_n.html')

    if item.user == request.user:
        return render(request, 'items/item_y.html', {'item': item, 'items': items})
    raise Http404

@method_decorator(login_required, name='dispatch')
class ItemCreateView(View):
    def get(self, request, *args, **kwargs):
        assets = at_tagging(request)
        items = Item.objects.filter(user=request.user).order_by('name')
        form = forms.ItemForm()
        return render(request, 'items/item_form.html', {
            'assets': assets,
            'items': items,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item/spell created!")
            return HttpResponseRedirect(item.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class ItemUpdateView(View):
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        if item.user == request.user:
            items = Item.objects.filter(user=request.user).order_by('name')
            form = forms.ItemForm(instance=item)
            return render(request, 'items/item_form.html', {
                'assets': at_tagging(request),
                'item': item,
                'items': items,
                'form': form,
            })
        raise Http404

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        if item.user == request.user:
            form = forms.ItemForm(instance=item, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated item/spell: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(item.get_absolute_url())
        raise Http404

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user == request.user:
        item.delete()
        messages.success(request, 'Item/spell deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('items:item_detail'))
    else:
        raise Http404

class ItemCopyView(View):
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        if item.user == request.user:
            create_item_copy(item, request.user)
            item.name += "_copy"
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item copied")
            return redirect(item.get_absolute_url())
        raise Http404

class ItemExport(View):
    def get(self, request, *args, **kwargs):
        queryset = Item.objects.filter(user=request.user).order_by('name')
        items = serializers.serialize("json", queryset, indent=2)
        return render(request, 'items/item_export.html', {'items': items})


class ItemImport(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'items/item_import.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')

            for obj in serializers.deserialize("json", user_import):
                obj.object.pk = None
                obj.object.user = request.user
                obj.object.save()
        return HttpResponseRedirect(reverse('items:item_detail'))
