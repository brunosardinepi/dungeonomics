from django import forms

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
            'content',
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
            'race',
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
            'content',
        ]

class PlayerForm(TinyMCEForm):
    class Meta:
        model = models.Player
        fields = [
            'player_name',
            'character_name',
            'level',
            'xp',
            'race',
            'character_class',
            'background',
            'alignment',
            'armor_class',
            'initiative',
            'speed',
            'proficiency_bonus',
            'hit_points',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'saving_throws',
            'skills',
            'age',
            'height',
            'weight',
            'languages',
            'personality',
            'ideals',
            'bonds',
            'flaws',
            'feats',
            'attacks',
            'spells',
            'proficiencies',
            'equipment',
            'notes',
        ]

class CopyMonsterForm(forms.ModelForm):
    class Meta:
        model = models.Monster
        fields = ['name']

class CopyNPCForm(forms.ModelForm):
    class Meta:
        model = models.NPC
        fields = ['name']

class CopyPlayerForm(forms.ModelForm):
    class Meta:
        model = models.Player
        fields = ['player_name']

class ImportMonsterForm(forms.ModelForm):
    class Meta:
        model = models.Monster
        fields = [
            'name',
        ]

class ImportNPCForm(forms.ModelForm):
    class Meta:
        model = models.NPC
        fields = [
            'name',
        ]

class SRDMonsterForm(forms.ModelForm):
    class Meta:
        model = models.Monster
        fields = ['name']

class SRDNPCForm(forms.ModelForm):
    class Meta:
        model = models.NPC
        fields = ['name']

MonsterFormSet = forms.modelformset_factory(
    models.Monster,
    form=MonsterForm,
    extra=0,
)

NPCFormSet = forms.modelformset_factory(
    models.NPC,
    form=NPCForm,
    extra=0,
)

class MonsterPublishForm(TinyMCEForm):
    class Meta:
        model = models.Monster
        fields = [
            'tavern_description',
        ]

class NPCPublishForm(TinyMCEForm):
    class Meta:
        model = models.NPC
        fields = [
            'tavern_description',
        ]

class PlayerPublishForm(TinyMCEForm):
    class Meta:
        model = models.Player
        fields = [
            'tavern_description',
        ]
