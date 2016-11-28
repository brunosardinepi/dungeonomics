from django.shortcuts import render
from django.views.generic import TemplateView

from allauth.account import views


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

    def __init__(self, *args, **kwargs):
        super(SignupView, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'The field is is is is is required'}


class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'confirm_email.html'


class EmailVerificationSentView(views.EmailVerificationSentView):
    template_name = 'verification_sent.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'password_reset.html'