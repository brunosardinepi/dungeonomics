from django import forms
from django.contrib.auth.models import User


class FormTemplate(forms.ModelForm):
    class Media:
        css = {
            'all': (
                'plugins/css/ace.min.css',
#                'martor/css/martor.bootstrap.min.css',
            ),
        }
        js = (
            'plugins/js/highlight.min.js',
        )

class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
