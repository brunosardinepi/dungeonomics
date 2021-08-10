from django import forms
from django.forms import inlineformset_factory
from tables import models


class HTMLForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/mention.js',
            )


class TableForm(HTMLForm):
    class Meta:
        model = models.Table
        fields = [
            'name',
            'content',
        ]

TableOptionFormSet = inlineformset_factory(
    models.Table,
    models.TableOption,
    fields=('content',),
    extra=0,
    min_num=2,
)
