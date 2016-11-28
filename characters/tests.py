from django.test import TestCase

from . import forms


class MonsterTestCase(TestCase):
    form_data = {
        'name': 'Sir Bearington',
        'level': 20,
        'alignment': 'LG',
        'size': 'Large',
        'languages': 'Common, Bear',
        'strength': 20,
        'dexterity': 20,
        'constitution': 20,
        'intelligence': 20,
        'wisdom': 20,
        'charisma': 20,
        'armor_class': 18,
        'hit_points': 100,
        'speed': '30 ft.',
        'saving_throws': 'None',
        'skills': 'Cunning',
        'creature_type': 'Bear',
        'damage_vulnerabilities': 'Fire',
        'damage_immunities': 'Slashing',
        'condition_immunities': 'Blind',
        'senses': 'Darkvision',
        'challenge_rating': 10,
        'traits': 'Looks like a bear, fights like a ninja',
        'actions': 'Attacks you',
        }

    def test_monster_form_success(self):
        """Successfully create a monster"""
        form = forms.MonsterForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_monster_form_bad_name(self):
        """Fail to create a monster because of no name"""
        form_data_test = dict(form_data)
        form_data_test['name'] = ''
        form = forms.MonsterForm(data=form_data_test)
        self.assertFalse(form.is_valid())

    def test_monster_form_bad_level(self):
        """Fail to create a monster because of no level"""
        form_data_test = dict(form_data)
        form_data_test['level'] = ''
        form = forms.MonsterForm(data=form_data_test)
        self.assertFalse(form.is_valid())


class NPCTestCase(TestCase):
    def test_npc_form_success(self):
        """Successfully create an NPC"""
        form_data = {
            'name': 'Deckard Cain',
            'level': 20,
            'alignment': 'LG',
            'size': 'Medium',
            'languages': 'Everything',
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 20,
            'wisdom': 20,
            'charisma': 20,
            'armor_class': 12,
            'hit_points': 34,
            'speed': '20 ft.',
            'saving_throws': 'None',
            'skills': 'Identify',
            'npc_class': 'Wizard',
            'age': 225,
            'height': '4 ft. 5 in.',
            'weight': '80 lbs.',
            'creature_type': 'Human',
            'damage_vulnerabilities': 'All',
            'damage_immunities': 'None',
            'condition_immunities': 'None',
            'senses': 'None',
            'challenge_rating': 20,
            'traits': 'Can identify any artifact with ease',
            'actions': 'Asks you to stay awhile and listen',
            'notes': 'Old man',
            }
        form = forms.NPCForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_npc_form_bad_name(self):
        """Fail to create an NPC because of no name"""
        form_data = {
            'name': '',
            'level': 20,
            'alignment': 'LG',
            'size': 'Medium',
            'languages': 'Everything',
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 20,
            'wisdom': 20,
            'charisma': 20,
            'armor_class': 12,
            'hit_points': 34,
            'speed': '20 ft.',
            'saving_throws': 'None',
            'skills': 'Identify',
            'npc_class': 'Wizard',
            'age': 225,
            'height': '4 ft. 5 in.',
            'weight': '80 lbs.',
            'creature_type': 'Human',
            'damage_vulnerabilities': 'All',
            'damage_immunities': 'None',
            'condition_immunities': 'None',
            'senses': 'None',
            'challenge_rating': 20,
            'traits': 'Can identify any artifact with ease',
            'actions': 'Asks you to stay awhile and listen',
            'notes': 'Old man',
            }
        form = forms.NPCForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_npc_form_bad_level(self):
        """Fail to create an NPC because of no level"""
        form_data = {
            'name': 'Deckard Cain',
            'level': '',
            'alignment': 'LG',
            'size': 'Medium',
            'languages': 'Everything',
            'strength': 10,
            'dexterity': 10,
            'constitution': 10,
            'intelligence': 20,
            'wisdom': 20,
            'charisma': 20,
            'armor_class': 12,
            'hit_points': 34,
            'speed': '20 ft.',
            'saving_throws': 'None',
            'skills': 'Identify',
            'npc_class': 'Wizard',
            'age': 225,
            'height': '4 ft. 5 in.',
            'weight': '80 lbs.',
            'creature_type': 'Human',
            'damage_vulnerabilities': 'All',
            'damage_immunities': 'None',
            'condition_immunities': 'None',
            'senses': 'None',
            'challenge_rating': 20,
            'traits': 'Can identify any artifact with ease',
            'actions': 'Asks you to stay awhile and listen',
            'notes': 'Old man',
            }
        form = forms.NPCForm(data=form_data)
        self.assertFalse(form.is_valid())