from django import forms
from django.contrib.auth.models import User

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        css = {
            'all': (
                '/static/css/autocomplete.css',
                'https://cdnjs.cloudflare.com/ajax/libs/at.js/1.5.2/css/jquery.atwho.min.css',
                )
            }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/at.js/1.5.2/js/jquery.atwho.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Caret.js/0.3.1/jquery.caret.min.js',
            '/static/js/tinymce/tinymce.min.js',
            )


class LocationForm(TinyMCEForm):
    class Meta:
        model = models.Location
        fields = [
            'name',
            'parent',
            'content',
        ]


class DeleteLocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = ['name']


LocationFormSet = forms.modelformset_factory(
    models.Location,
    form=LocationForm,
    extra=0,
)

#LocationInlineFormSet = forms.inlineformset_factory(
#    models.World,
#    models.Location,
#    extra=0,
#    fields=('name',),
#    formset=LocationFormSet,
#)
