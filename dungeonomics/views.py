from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from allauth.account import views

from . import forms


class HomeView(TemplateView):
    template_name = 'home.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'


# class LogoutView(views.LogoutView):
#     template_name = 'logout.html'


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
def delete_account(request):  
    pk = request.user.id
    user = User.objects.get(pk=pk)
    user_form = forms.DeleteUserForm(instance=user)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = DeleteUserForm(request.POST, instance=user)
            if user_form.is_valid():
                deactivate_user = user_form.save(commit=False)
                user.is_active = False
                deactivate_user.save()
        return render(request, "delete_account.html", {'user_form': user_form})
    else:
        raise PermissionDenied