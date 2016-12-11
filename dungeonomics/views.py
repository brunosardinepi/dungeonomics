from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from allauth.account import views

from . import forms
from campaign import models as campaign_models
from characters import models as character_models


class HomeView(TemplateView):
    template_name = 'home.html'


# class ProfileView(TemplateView):
#     template_name = 'profile.html'

@login_required
def profile_detail(request):
    user = get_object_or_404(User, pk=request.user.pk)
    campaigns = campaign_models.Campaign.objects.filter(user=user).count()
    monsters = character_models.Monster.objects.filter(user=user).count()
    npcs = character_models.NPC.objects.filter(user=user).count()
    return render(request, 'profile.html', {'user': user, 'campaigns': campaigns, 'monsters': monsters, 'npcs': npcs})

class LoginView(views.LoginView):
    template_name = 'login.html'


class SignupView(views.SignupView):
    template_name = 'signup.html'


class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'confirm_email.html'


class EmailVerificationSentView(views.EmailVerificationSentView):
    template_name = 'verification_sent.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'password_reset.html'


@login_required
def account_delete(request):
    user = get_object_or_404(User, pk=request.user.pk)
    form = forms.DeleteUserForm(instance=user)
    if request.method == 'POST':
        form = forms.DeleteUserForm(request.POST, instance=user)
        # if form.is_valid() and user.pk == request.user.pk:
        if user.pk == request.user.pk:
        # if form.is_valid():
            user.delete()
            return HttpResponseRedirect('home')
    return render(request, 'delete_account.html', {'form': form, 'user': user})


class PasswordResetDoneView(TemplateView):
    template_name = "password_reset_done.html"


class CustomPasswordResetFromKeyView(views.PasswordResetFromKeyView):
    template_name = "password_reset_from_key.html"



class PasswordResetFromKeyDoneView(TemplateView):
    template_name = "password_reset_from_key_done.html"


def error_404_view(request):
    return render(request, 'error_404.html')