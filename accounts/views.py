from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic, View
from django.views.generic import TemplateView

from . import forms


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class Signup(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


def deactivate_user_view(request):
    user = User.objects.get(pk=request.user.pk)
    form = forms.DeactivateUserForm(instance=user)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            form = forms.DeactivateUserForm(request.POST, instance=user)
            if form.is_valid():
                deactivate_user = form.save(commit=False)
                user.is_active = False
                deactivate_user.save()
                messages.add_message(request, messages.SUCCESS, "Account deleted!")
                return HttpResponseRedirect(reverse_lazy('accounts:logout'))
        return render(request, "accounts/account_confirm_delete.html", {
            "form": form,
        })