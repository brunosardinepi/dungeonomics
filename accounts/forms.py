from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email Address"
        self.fields['email'].required = True


class DeactivateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

    def clean_is_active(self):  
        # Reverses true/false for your form prior to validation
        #
        # You can also raise a ValidationError here if you receive 
        # a value you don't want, to prevent the form's is_valid 
        # method from return true if, say, the user hasn't chosen 
        # to deactivate their account
        is_active = not(self.cleaned_data["is_active"])
        return is_active