from itertools import chain
from shutil import copyfile
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from . import forms
from . import models
from characters import models as character_models
from dungeonomics import settings
from dungeonomics.utils import at_tagging, image_is_valid
from items import models as item_models


@login_required
def location_detail(request, world_pk=None, location_pk=None):
    worlds = sorted(models.World.objects.filter(user=request.user), key=lambda world: world.name.lower())
    if world_pk:
        world = get_object_or_404(models.World, pk=world_pk)
        if world.user == request.user:
            return render(request, 'locations/location_detail.html', {
                'world': world,
                'worlds': worlds,
            })
        else:
            raise Http404
    elif location_pk:
        location = get_object_or_404(models.Location, pk=location_pk)
        if location.user == request.user:
            return render(request, 'locations/location_detail.html', {
                'location': location,
                'worlds': worlds,
            })
        else:
            raise Http404
    else:
        world = None
        if len(worlds) > 0:
            world = worlds[0]
        return render(request, 'locations/location_detail.html', {
            'world': world,
            'worlds': worlds,
        })

class WorldCreate(LoginRequiredMixin, CreateView):
    model = models.World
    form_class = forms.WorldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the objects to be used in mentions.
        context['data'] = at_tagging(self.request)

        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)

        # Send the request object to the form.
        kwargs['request'] = self.request

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)

            # Set the object's user.
            self.object.user = request.user

            if form.cleaned_data['image']:
                image_validity_check = image_is_valid(request, form)
                if image_validity_check == True:
                    self.object.image = form.cleaned_data['image']
                elif (
                    image_validity_check == "bad size" or
                    image_validity_check == "bad type"
                ):
                    return self.form_invalid(form)
            return self.form_valid(form)

@login_required
def location_create(request, world_pk, location_pk=None):
    data = at_tagging(request)
    world = get_object_or_404(models.World, pk=world_pk)
    if world.user == request.user:
        initial = {'world': world}
        if location_pk:
            parent_location = get_object_or_404(models.Location, pk=location_pk)
            initial['parent_location'] = parent_location
        form = forms.LocationForm(request.user.pk, world_pk, location_pk, initial=initial)
        if request.method == 'POST':
            form = forms.LocationForm(request.user.pk, world_pk, location_pk, request.POST, request.FILES, initial=initial)
            if form.is_valid():
                location = form.save(commit=False)
                if location_pk:
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

    return render(request, 'locations/location_form.html', {
        'data': data,
        'world': world,
        'form': form,
    })

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

class WorldsDelete(View):
    def get(self, request, *args, **kwargs):
        worlds = models.World.objects.filter(user=request.user).order_by('name')
        return render(request, 'locations/worlds_delete.html', {'worlds': worlds})

    def post(self, request, *args, **kwargs):
        for world_pk in request.POST.getlist('world'):
            models.World.objects.get(pk=world_pk).delete()
        return HttpResponseRedirect(reverse('locations:location_detail'))

class WorldExport(View):
    def get(self, request, *args, **kwargs):
        worlds = models.World.objects.filter(user=request.user).order_by('name')
        locations = models.Location.objects.filter(user=request.user).order_by('name')

        combined_list = list(chain(worlds, locations))
        worlds_locations = serializers.serialize("json", combined_list, indent=2)

        return render(request,
            'locations/world_export.html',
            {'worlds_locations': worlds_locations},
        )

class WorldImport(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'locations/world_import.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')

            asset_references = {
                "worlds": {},
                "locations": {},
            }

            # create a copy of the asset
            # and update a dictionary that holds a reference of the old pk and the new pk

            for obj in serializers.deserialize("json", user_import):
                # grab the old pk for reference
                old_pk = obj.object.pk

                # create a copy of the asset
                obj.object.pk = None
                obj.object.user = request.user

                if obj.object.image:
                    # create a new filename
                    random_string = models.create_random_string()
                    ext = obj.object.image.url.split('.')[-1]
                    new_filename = "media/user/images/%s.%s" % (random_string, ext)

                    # copy the old file to a new file
                    # and save it to the new object
                    old_image_url = settings.MEDIA_ROOT + obj.object.image.name
                    new_image_url = settings.MEDIA_ROOT + new_filename
                    copyfile(old_image_url, new_image_url)
                    obj.object.image = new_filename

                obj.object.save()

                new_pk = obj.object.pk

                if isinstance(obj.object, models.World):
                    asset_references['worlds'][old_pk] = new_pk
                elif isinstance(obj.object, models.Location):
                    asset_references['locations'][old_pk] = new_pk

            for old_pk, new_pk in asset_references['locations'].items():
                # for each location, set the parent location to the new parent location.
                # also, set the world to the new world
                old_location = models.Location.objects.get(pk=old_pk)
                if old_location.parent_location:
                    old_location_parent = old_location.parent_location

                new_location = models.Location.objects.get(pk=new_pk)
                if new_location.parent_location:
                    new_location_parent = models.Location.objects.get(pk=asset_references['locations'][old_location_parent.pk])
                    new_location.parent_location = new_location_parent

                old_world = old_location.world
                new_world = models.World.objects.get(pk=asset_references['worlds'][old_world.pk])
                new_location.world = new_world
                new_location.save()
            return redirect(new_world.get_absolute_url())
        return redirect('locations:location_detail')
