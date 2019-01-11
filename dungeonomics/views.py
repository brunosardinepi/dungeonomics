from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from allauth.account import views

from . import forms
from allauth.account import models as allauth_models
from campaign.models import Campaign
from characters.models import GeneralCharacter
from characters.utils import create_character_copy, get_character_stats, get_characters
from items.models import Item
from locations.models import Location, World
from tables.models import Table
from votes.models import Feature, Vote


class HomeView(TemplateView):
    template_name = 'home.html'


def home_view(request):
    if request.user.is_authenticated:
        features = Feature.objects.all().annotate(votes=Count('vote')).order_by('-votes')
        return render(request, 'home.html', {'features': features})
    else:
        users = allauth_models.EmailAddress.objects.count()
        campaigns = Campaign.objects.count()
        characters = GeneralCharacter.objects.count()
        return render(request, 'home.html', {
            'users': users,
            'campaigns': campaigns,
            'characters': characters,
        })

@login_required
def profile_detail(request):
    user = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'profile.html', {'user': user })

@login_required
def srd(request, active_asset_type=None):
    characters = get_characters(3029)
    items = Item.objects.filter(user=3029)

    assets = OrderedDict([
        ('Characters', characters),
        ('Items', items),
    ])

    if request.method == 'POST':
        for pk in request.POST.getlist('character'):
            character = GeneralCharacter.objects.get(pk=pk)
            create_character_copy(character, request.user)
        for pk in request.POST.getlist('item'):
            item = Item.objects.get(pk=pk)
            item.pk = None
            item.user = request.user
            item.save()

        # find the most imported assets and redirec to that detail page
        if len(request.POST.getlist('character')) >= len(request.POST.getlist('item')):
            return redirect('characters:character_detail')
        else:
            return redirect('items:item_detail')

    if not active_asset_type:
        active_asset_type = next(iter(assets))
    else:
        active_asset_type = active_asset_type.capitalize()

    if active_asset_type == "Characters":
        active_assets = GeneralCharacter.objects.filter(user=3029).order_by('name')
    elif active_asset_type == "Items":
        active_assets = items

    data = {
        'assets': assets,
        'active_asset_type': active_asset_type,
        'active_assets': active_assets,
    }
    return render(request, 'srd.html', data)

@login_required
def srd_assets(request):
    """Get a list of assets based on an asset type"""

    asset_type = request.GET.get("asset_type")

    if asset_type == "Characters":
        assets = GeneralCharacter.objects.filter(user=3029).order_by('name')
    elif asset_type == "Items":
        assets = Item.objects.filter(user=3029).order_by('name')

    html = render(request, "srd_assets.html", {
        'assets': assets,
        'asset_type': asset_type,
    })
    return HttpResponse(html)

@login_required
def srd_asset(request):
    """Get an individual asset's stats"""

    asset_type = request.GET.get("asset_type")
    asset_pk = request.GET.get("pk")

    if asset_type == "Characters":
        asset = get_object_or_404(GeneralCharacter, pk=asset_pk)
        html = render(request, "characters/character_stats.html", {
            'character': asset,
            'stats': get_character_stats(asset),
        })
    elif asset_type == "Items":
        asset = get_object_or_404(Item, pk=asset_pk)
        html = render(request, "items/item_stats.html", {'item': asset})
    elif asset_type == "Worlds":
        asset = get_object_or_404(World, pk=asset_pk)
        html = render(request, "locations/location_stats.html", {'location': asset})
    elif asset_type == "Locations":
        asset = get_object_or_404(Location, pk=asset_pk)
        html = render(request, "locations/location_stats.html", {'location': asset})
    elif asset_type == "Tables":
        asset = get_object_or_404(Table, pk=asset_pk)
        html = render(request, "tables/table_stats.html", {'table': asset})

    return HttpResponse(html)

@login_required
def srd_tools_update(request):
    """Update col tools when an asset is added/removed"""

    col = request.GET.get("col")
    action = request.GET.get("action")

    if col == "3":
        if action == "add":
            html = render(request, "srd_col3_tools_add.html")
        elif action == "remove":
            html = render(request, "srd_col3_tools_remove.html")

    return HttpResponse(html)

@login_required
def resources(request, active_asset_type=None):
    items = Item.objects.filter(user=request.user)
    worlds = World.objects.filter(user=request.user)
    tables = Table.objects.filter(user=request.user)

    assets = OrderedDict([
        ('Items', items),
        ('Worlds', worlds),
        ('Tables', tables),
    ])

    if not active_asset_type:
        active_asset_type = next(iter(assets))
    else:
        active_asset_type = active_asset_type.capitalize()

    if active_asset_type == "Items":
        active_assets = items
    elif active_asset_type == "Worlds":
        active_assets = worlds
    elif active_asset_type == "Tables":
        active_assets = tables

    active_asset = active_assets.first()

    data = {
        'assets': assets,
        'active_asset_type': active_asset_type,
        'active_assets': active_assets,
        'active_asset': active_asset,
    }
    return render(request, 'resources.html', data)

@login_required
def resources_assets(request):
    """Get a list of assets based on an asset type"""

    asset_type = request.GET.get("asset_type")

    if asset_type == "Items":
        assets = Item.objects.filter(user=request.user).order_by('name')
    elif asset_type == "Worlds":
        assets = OrderedDict()
        worlds = World.objects.filter(user=request.user).order_by('name')
        for world in worlds:
            locations = Location.objects.filter(world=world).order_by('name')
            assets[world] = locations
    elif asset_type == "Tables":
        assets = Table.objects.filter(user=request.user).order_by('name')

    if asset_type == "Worlds":
        html = render(request, "resources_assets_worlds.html", {
            'assets': assets,
            'asset_type': asset_type,
        })
    else:
        html = render(request, "resources_assets.html", {
            'assets': assets,
            'asset_type': asset_type,
        })

    return HttpResponse(html)

@login_required
def resources_tools_update(request):
    """Update col tools when a resource type is selected"""

    col = request.GET.get("col")
    resource_type = request.GET.get("resource_type")

    html = render(request, "resources_col{}_tools_{}.html".format(
        col,
        resource_type.lower(),
    ))

    return HttpResponse(html)

class LoginView(views.LoginView):
    template_name = 'login.html'


class SignupView(views.SignupView):
    template_name = 'signup.html'


class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'confirm_email.html'


class EmailVerificationSentView(views.EmailVerificationSentView):
    template_name = 'verification_sent.html'


class EmailView(views.EmailView):
    template_name = 'email.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'password_reset.html'


@login_required
def account_delete(request):
    user = get_object_or_404(User, pk=request.user.pk)
    if user == request.user:
        user.delete()
        return HttpResponseRedirect('home')
    else:
        raise Http404

class PasswordResetDoneView(TemplateView):
    template_name = "password_reset_done.html"


class CustomPasswordResetFromKeyView(views.PasswordResetFromKeyView):
    template_name = "password_reset_from_key.html"


class PasswordResetFromKeyDoneView(TemplateView):
    template_name = "password_reset_from_key_done.html"


def handler400(request):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


class DonateView(TemplateView):
    template_name = 'donate.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'
