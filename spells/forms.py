from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )


class SpellForm(TinyMCEForm):
    class Meta:
        model = models.Spell
        fields = [
            'name',
            'spell_type',
            'rarity',
            'description',
        ]


class DeleteSpellForm(forms.ModelForm):
    class Meta:
        model = models.Spell
        fields = ['name']


class CopySpellForm(forms.ModelForm):
    class Meta:
        model = models.Spell
        fields = ['name']
