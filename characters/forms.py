from django import forms

from . import models


class MonsterForm(forms.ModelForm):
    class Meta:
        model = models.Monster
        fields = [
            'name',
            'level',
            'alignment',
        ]


class NPCForm(forms.ModelForm):
    class Meta:
        model = models.NPC
        fields = [
            'name',
            'level',
            'alignment',
        ]