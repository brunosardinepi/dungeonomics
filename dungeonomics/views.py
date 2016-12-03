from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
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
        if form.is_valid() and user == request.user:
            user.delete()
            messages.add_message(request, messages.SUCCESS, "Deleted user!")
            return HttpResponseRedirect('home')
    return render(request, 'delete_account.html', {'form': form, 'user': user})