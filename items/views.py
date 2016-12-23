from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from . import forms
from . import models


@login_required
def item_detail(request, item_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    items = sorted(models.MagicItem.objects.filter(user=user),
        key=lambda item: item.name.lower()
        )
    if item_pk:
        this_item = get_object_or_404(models.MagicItem, pk=item_pk)
        if this_item.user == request.user:
            return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})
        else:
            raise Http404
    elif len(items) > 0:
        this_item = items[0]
        if this_item.user == request.user:
            return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})
        else:
            raise Http404
    else:
        this_item = None
    return render(request, 'items/item_detail.html', {'this_item': this_item, 'items': items})

@login_required
def item_create(request):
    form = forms.ItemForm()
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.add_message(request, messages.SUCCESS, "Item created!")
            return HttpResponseRedirect(item.get_absolute_url())
    return render(request, 'items/item_form.html', {'form': form})

@login_required
def item_update(request, item_pk):
    item = get_object_or_404(models.MagicItem, pk=item_pk)
    if item.user == request.user:
        form = forms.ItemForm(instance=item)
        if request.method == 'POST':
            form = forms.ItemForm(instance=item, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated item: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    return render(request, 'items/item_form.html', {'form': form, 'item': item})

@login_required
def item_delete(request, item_pk):
    item = get_object_or_404(models.MagicItem, pk=item_pk)
    if item.user == request.user:
        form = forms.DeleteItemForm(instance=item)
        if request.method == 'POST':
            form = forms.DeleteItemForm(request.POST, instance=item)
            if item.user.pk == request.user.pk:
                item.delete()
                messages.add_message(request, messages.SUCCESS, "Item deleted!")
                return HttpResponseRedirect(reverse('items:item_detail'))
    else:
        raise Http404
    return render(request, 'items/item_delete.html', {'form': form, 'item': item})

@login_required
def item_copy(request, item_pk):
    item = get_object_or_404(models.MagicItem, pk=item_pk)
    if item.user == request.user:
        form = forms.CopyItemForm(instance=item)
        if request.method == 'POST':
            form = forms.CopyItemForm(request.POST, instance=item)
            if item.user.pk == request.user.pk:
                item.pk = None
                item.name = item.name + "_Copy"
                item.save()
                messages.add_message(request, messages.SUCCESS, "Item copied!")
                return HttpResponseRedirect(item.get_absolute_url())
    else:
        raise Http404
    return render(request, 'items/item_copy.html', {'form': form, 'item': item})