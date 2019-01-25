from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from allauth.account import views

from . import forms
from allauth.account import models as allauth_models
from campaign import models as campaign_models
from characters import models as character_models
from votes.models import Feature, Vote


class HomeView(TemplateView):
    template_name = 'home.html'


def home_view(request):
    if request.user.is_authenticated:
        features = Feature.objects.all().annotate(votes=Count('vote')).order_by('-votes')
        return render(request, 'home.html', {'features': features})
    else:
        users = allauth_models.EmailAddress.objects.count()
        campaigns = campaign_models.Campaign.objects.count()
        monsters = character_models.Monster.objects.count()
        npcs = character_models.NPC.objects.count()
        characters = monsters + npcs
        return render(request, 'home.html', {'users': users, 'campaigns': campaigns, 'characters': characters})

@login_required
def profile_detail(request):
    user = get_object_or_404(User, pk=request.user.pk)
    campaigns = campaign_models.Campaign.objects.filter(user=user).count()
    monsters = character_models.Monster.objects.filter(user=user).count()
    npcs = character_models.NPC.objects.filter(user=user).count()
    return render(request, 'profile.html', {'user': user, 'campaigns': campaigns, 'monsters': monsters, 'npcs': npcs})

class SocialAuthView(TemplateView):
    template_name = "social_auth.html"

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
