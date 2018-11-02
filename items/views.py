from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View

from . import forms
from . import models

from characters import models as character_models
from dungeonomics.utils import at_tagging
from locations import models as location_models


@login_required
def item_detail(request, item_pk=None):
    user = None
    if request.user.is_authenticated:
        user = request.user.pk
    items = sorted(models.Item.objects.filter(user=user), key=lambda item: item.name.lower())
    if item_pk:
        item = get_object_or_404(models.Item, pk=item_pk)
        if item.user == request.user:
            return render(request, 'items/item_detail.html', {'item': item, 'items': items})
        else:
            raise Http404
    elif len(items) > 0:
        item = items[0]
        if item.user == request.user:
            return render(request, 'items/item_detail.html', {'item': item, 'items': items})
        else:
            raise Http404
    else:
        item = None
    return render(request, 'items/item_detail.html', {'item': item, 'items': items})

@login_required
def item_create(request):
    data = at_tagging(request)
    form = forms.ItemForm()
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item/spell created!")
            return HttpResponseRedirect(item.get_absolute_url())
    data['form'] = form
    return render(request, 'items/item_form.html', data)

@login_required
def item_update(request, item_pk):
    data = at_tagging(request)
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        form = forms.ItemForm(instance=item)
        if request.method == 'POST':
            form = forms.ItemForm(instance=item, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated item/spell: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    data['form'] = form
    data['item'] = item
    return render(request, 'items/item_form.html', data)

@login_required
def item_delete(request, item_pk):
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        item.delete()
        messages.success(request, 'Item/spell deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('items:item_detail'))
    else:
        raise Http404

@login_required
def item_copy(request, item_pk):
    item = get_object_or_404(models.Item, pk=item_pk)
    if item.user == request.user:
        form = forms.CopyItemForm(instance=item)
        if request.method == 'POST':
            form = forms.CopyItemForm(request.POST, instance=item)
            if item.user.pk == request.user.pk:
                item.pk = None
                item.name = item.name + "_Copy"
                item.save()
                messages.add_message(request, messages.SUCCESS, "Item/spell copied!")
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    return render(request, 'items/item_copy.html', {'form': form, 'item': item})

class ItemsDelete(View):
    def get(self, request, *args, **kwargs):
        items = models.Item.objects.filter(user=request.user).order_by('name')
        return render(request, 'items/items_delete.html', {'items': items})

    def post(self, request, *args, **kwargs):
        for item_pk in request.POST.getlist('item'):
            models.Item.objects.get(pk=item_pk).delete()
        return HttpResponseRedirect(reverse('items:item_detail'))

class ItemExport(View):
    def get(self, request, *args, **kwargs):
        queryset = models.Item.objects.filter(user=request.user).order_by('name')
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
