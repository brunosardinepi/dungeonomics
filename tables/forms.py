from django import forms
from django.forms import inlineformset_factory

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


class TableForm(TinyMCEForm):
    class Meta:
        model = models.Table
        fields = [
            'name',
            'description',
        ]

TableOptionFormSet = inlineformset_factory(
    models.Table,
    models.TableOption,
    fields=('description',),
    extra=0,
    min_num=2,
)