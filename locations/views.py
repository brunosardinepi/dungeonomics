from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms
from . import models
from characters import models as character_models
from dungeonomics.utils import at_tagging, image_is_valid
from items import models as item_models

import json


@login_required
def location_detail(request, world_pk=None, location_pk=None):
    worlds = sorted(models.World.objects.filter(user=request.user), key=lambda world: world.name.lower())
    if world_pk:
        world = get_object_or_404(models.World, pk=world_pk)
        if world.user == request.user:
            return render(request, 'locations/location_detail.html', {'world': world, 'worlds': worlds})
        else:
            raise Http404
    elif location_pk:
        location = get_object_or_404(models.Location, pk=location_pk)
        if location.user == request.user:
            return render(request, 'locations/location_detail.html', {'location': location, 'worlds': worlds})
        else:
            raise Http404
    else:
        world = None
        if len(worlds) > 0:
            world = worlds[0]
        return render(request, 'locations/location_detail.html', {'world': world, 'worlds': worlds})

@login_required
def world_create(request):
    data = at_tagging(request)
    form = forms.WorldForm()
    if request.method == 'POST':
        form = forms.WorldForm(request.POST, request.FILES)
        if form.is_valid():
            world = form.save(commit=False)
            world.user = request.user
            if form.cleaned_data['image']:
                image_validity_check = image_is_valid(request, form)
                if image_validity_check == True:
                    world.image = form.cleaned_data['image']
                elif image_validity_check == "bad size":
                    return redirect('/error/image-size/')
                elif image_validity_check == "bad type":
                    return redirect('/error/image-type/')
            world.save()
            messages.add_message(request, messages.SUCCESS, "World created!")
            return HttpResponseRedirect(world.get_absolute_url())
    data['form'] = form
    return render(request, 'locations/world_form.html', data)

@login_required
def location_create(request, world_pk, location_pk=None):
    data = at_tagging(request)
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        form = forms.LocationForm(request.user.pk, world_pk, location_pk, initial={'world': world})
        if request.method == 'POST':
            form = forms.LocationForm(request.user.pk, world_pk, location_pk, request.POST, request.FILES, initial={'world': world})
            if form.is_valid():
                location = form.save(commit=False)
                if location_pk:
                    parent_location = get_object_or_404(models.Location, pk=location_pk)
                    if parent_location.user == request.user:
                        location.parent = parent_location
                location.user = request.user

                if form.cleaned_data['image']:
                    image_validity_check = image_is_valid(request, form)
                    if image_validity_check == True:
                        location.image = form.cleaned_data['image']
                    elif image_validity_check == "bad size":
                        return redirect('/error/image-size/')
                    elif image_validity_check == "bad type":
                        return redirect('/error/image-type/')

                location.world = world
                location.save()
                messages.add_message(request, messages.SUCCESS, "Location created!")
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    data['world'] = world
    data['form'] = form
    return render(request, 'locations/location_form.html', data)

@login_required
def world_update(request, world_pk):
    data = at_tagging(request)
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        form = forms.WorldForm(instance=world)
        location_forms = forms.LocationInlineFormSet(queryset=form.instance.location_set.all())
        if request.method == 'POST':
            form = forms.WorldForm(request.POST, request.FILES, instance=world)
            location_forms = forms.LocationInlineFormSet(request.POST, request.FILES, queryset=form.instance.location_set.all())
            if form.is_valid() and location_forms.is_valid():

                if form.cleaned_data['image']:
                    image_validity_check = image_is_valid(request, form)
                    if image_validity_check == True:
                        pass
                    elif image_validity_check == "bad size":
                        return redirect('/error/image-size/')
                    elif image_validity_check == "bad type":
                        return redirect('/error/image-type/')

                form.save()
                locations = location_forms.save(commit=False)
                for location in locations:
                    location.world = world
                    location.user = request.user
                    location.save()
                for location in location_forms.deleted_objects:
                    location.delete()
                messages.add_message(request, messages.SUCCESS, "Updated world: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(world.get_absolute_url())
    else:
        raise Http404
    data['world'] = world
    data['form'] = form
    data['formset'] = location_forms
    return render(request, 'locations/world_form.html', data)

@login_required
def location_update(request, location_pk):
    data = at_tagging(request)
    location = get_object_or_404(models.Location, pk=location_pk)
    if location.user == request.user:
        form = forms.LocationForm(request.user.pk, location.world.pk, location_pk, instance=location)
        if request.method == 'POST':
            form = forms.LocationForm(request.user.pk, location.world.pk, location_pk, request.POST, request.FILES, instance=location)
            if form.is_valid():

                if form.cleaned_data['image']:
                    image_validity_check = image_is_valid(request, form)
                    if image_validity_check == True:
                        pass
                    elif image_validity_check == "bad size":
                        return redirect('/error/image-size/')
                    elif image_validity_check == "bad type":
                        return redirect('/error/image-type/')

                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated location: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(location.get_absolute_url())
    else:
        raise Http404
    data['location'] = location
    data['world'] = location.world
    data['form'] = form
    return render(request, 'locations/location_form.html', data)

@login_required
def world_delete(request, world_pk):
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        world.delete()
        messages.success(request, 'World deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('locations:location_detail'))
    else:
        raise Http404

@login_required
def location_delete(request, location_pk):
    location = get_object_or_404(models.Location, pk=location_pk)
    if location.user == request.user:
        location.delete()
        messages.success(request, 'Location deleted', fail_silently=True)
        return HttpResponseRedirect(reverse('locations:location_detail'))
    else:
        raise Http404