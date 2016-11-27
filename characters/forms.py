from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )


class MonsterForm(TinyMCEForm):
    class Meta:
        model = models.Monster
        fields = [
            'name',
            'level',
            'alignment',
        ]


class NPCForm(TinyMCEForm):
    class Meta:
        model = models.NPC
        fields = [
            'name',
            'level',
            'alignment',
        ]