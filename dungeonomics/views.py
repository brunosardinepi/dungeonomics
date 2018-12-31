from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from allauth.account import views

from . import forms
from allauth.account import models as allauth_models
from campaign.models import Campaign
from characters.models import GeneralCharacter
from characters.utils import create_character_copy, get_characters
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
def srd(request):
    characters = get_characters(3029)

    assets = {
        'Characters': characters,
    }

    if request.method == 'POST':
        for pk in request.POST.getlist('character'):
            character = GeneralCharacter.objects.get(pk=pk)
            create_character_copy(character, request.user)
        return redirect('characters:character_detail')

    active_asset_type = next(iter(assets))

    if active_asset_type == "Characters":
        active_assets = GeneralCharacter.objects.filter(user=3029).order_by('name')

    data = {
        'assets': assets,
        'active_asset_type': active_asset_type,
        'active_assets': active_assets,
        'characters': characters,
    }
    return render(request, 'srd.html', data)

@login_required
def srd_assets(request):
    # get the url parameters
    asset_type = request.GET.get("asset_type")

    # get the asset type's assets
    if asset_type == "Characters":
        assets = GeneralCharacter.objects.filter(user=3029).order_by('name')

    # render the html and pass it back to ajax
    html = render(request, "srd_assets.html", {'assets': assets})
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
