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
            'alignment',
            'size',
            'languages',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'armor_class',
            'hit_points',
            'speed',
            'saving_throws',
            'skills',
            'creature_type',
            'damage_vulnerabilities',
            'damage_immunities',
            'damage_resistances',
            'condition_immunities',
            'senses',
            'challenge_rating',
            'traits',
            'actions',
        ]


class NPCForm(TinyMCEForm):
    class Meta:
        model = models.NPC
        fields = [
            'name',
            'alignment',
            'size',
            'languages',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'armor_class',
            'hit_points',
            'speed',
            'saving_throws',
            'skills',
            'npc_class',
            'age',
            'height',
            'weight',
            'creature_type',
            'damage_vulnerabilities',
            'damage_immunities',
            'damage_resistances',
            'condition_immunities',
            'senses',
            'challenge_rating',
            'traits',
            'actions',
            'notes',
        ]


class DeleteMonsterForm(forms.ModelForm):
    class Meta:
        model = models.Monster
        fields = ['name']


class DeleteNPCForm(forms.ModelForm):
    class Meta:
        model = models.NPC
        fields = ['name']