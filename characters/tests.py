from django.test import TestCase

from . import forms


# class MonsterTestCase(TestCase):
#     form_data = {
#         'name': 'Sir Bearington',
#         'level': 20,
#         'alignment': 'LG',
#         'size': 'Large',
#         'languages': 'Common, Bear',
#         'strength': 20,
#         'dexterity': 20,
#         'constitution': 20,
#         'intelligence': 20,
#         'wisdom': 20,
#         'charisma': 20,
#         'armor_class': 18,
#         'hit_points': 100,
#         'speed': '30 ft.',
#         'saving_throws': 'None',
#         'skills': 'Cunning',
#         'creature_type': 'Bear',
#         'damage_vulnerabilities': 'Fire',
#         'damage_immunities': 'Slashing',
#         'condition_immunities': 'Blind',
#         'senses': 'Darkvision',
#         'challenge_rating': 10,
#         'traits': 'Looks like a bear, fights like a ninja',
#         'actions': 'Attacks you',
#         }

#     def test_monster_form_success(self):
#         """Successfully create a monster"""
#         form = forms.MonsterForm(data=self.form_data)
#         self.assertTrue(form.is_valid())

#     def test_monster_form_bad_name(self):
#         """Fail to create a monster because of no name"""
#         form_data_test = dict(self.form_data)
#         form_data_test['name'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_level(self):
#         """Fail to create a monster because of no level"""
#         form_data_test = dict(self.form_data)
#         form_data_test['level'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_alignment(self):
#         """Fail to create a monster because of no alignment"""
#         form_data_test = dict(self.form_data)
#         form_data_test['alignment'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_size(self):
#         """Fail to create a monster because of no size"""
#         form_data_test = dict(self.form_data)
#         form_data_test['size'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_languages(self):
#         """Fail to create a monster because of no languages"""
#         form_data_test = dict(self.form_data)
#         form_data_test['languages'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_strength(self):
#         """Fail to create a monster because of no strength"""
#         form_data_test = dict(self.form_data)
#         form_data_test['strength'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_dexterity(self):
#         """Fail to create a monster because of no dexterity"""
#         form_data_test = dict(self.form_data)
#         form_data_test['dexterity'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_constitution(self):
#         """Fail to create a monster because of no constitution"""
#         form_data_test = dict(self.form_data)
#         form_data_test['constitution'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_intelligence(self):
#         """Fail to create a monster because of no intelligence"""
#         form_data_test = dict(self.form_data)
#         form_data_test['intelligence'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_wisdom(self):
#         """Fail to create a monster because of no wisdom"""
#         form_data_test = dict(self.form_data)
#         form_data_test['wisdom'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_charisma(self):
#         """Fail to create a monster because of no charisma"""
#         form_data_test = dict(self.form_data)
#         form_data_test['charisma'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_armor_class(self):
#         """Fail to create a monster because of no armor_class"""
#         form_data_test = dict(self.form_data)
#         form_data_test['armor_class'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_hit_points(self):
#         """Fail to create a monster because of no hit_points"""
#         form_data_test = dict(self.form_data)
#         form_data_test['hit_points'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_speed(self):
#         """Fail to create a monster because of no speed"""
#         form_data_test = dict(self.form_data)
#         form_data_test['speed'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_saving_throws(self):
#         """Fail to create a monster because of no saving_throws"""
#         form_data_test = dict(self.form_data)
#         form_data_test['saving_throws'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_skills(self):
#         """Fail to create a monster because of no skills"""
#         form_data_test = dict(self.form_data)
#         form_data_test['skills'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_creature_type(self):
#         """Fail to create a monster because of no creature_type"""
#         form_data_test = dict(self.form_data)
#         form_data_test['creature_type'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_damage_vulnerabilities(self):
#         """Fail to create a monster because of no damage_vulnerabilities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['damage_vulnerabilities'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_damage_immunities(self):
#         """Fail to create a monster because of no damage_immunities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['damage_immunities'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_condition_immunities(self):
#         """Fail to create a monster because of no condition_immunities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['condition_immunities'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_senses(self):
#         """Fail to create a monster because of no senses"""
#         form_data_test = dict(self.form_data)
#         form_data_test['senses'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_monster_form_bad_challenge_rating(self):
#         """Fail to create a monster because of no challenge_rating"""
#         form_data_test = dict(self.form_data)
#         form_data_test['challenge_rating'] = ''
#         form = forms.MonsterForm(data=form_data_test)
#         self.assertFalse(form.is_valid())


# class NPCTestCase(TestCase):
#     form_data = {
#         'name': 'Deckard Cain',
#         'level': 20,
#         'alignment': 'LG',
#         'size': 'Medium',
#         'languages': 'Everything',
#         'strength': 10,
#         'dexterity': 10,
#         'constitution': 10,
#         'intelligence': 20,
#         'wisdom': 20,
#         'charisma': 20,
#         'armor_class': 12,
#         'hit_points': 34,
#         'speed': '20 ft.',
#         'saving_throws': 'None',
#         'skills': 'Identify',
#         'npc_class': 'Wizard',
#         'age': 225,
#         'height': '4 ft. 5 in.',
#         'weight': '80 lbs.',
#         'creature_type': 'Human',
#         'damage_vulnerabilities': 'All',
#         'damage_immunities': 'None',
#         'condition_immunities': 'None',
#         'senses': 'None',
#         'challenge_rating': 20,
#         'traits': 'Can identify any artifact with ease',
#         'actions': 'Asks you to stay awhile and listen',
#         'notes': 'Old man',
#         }
#     def test_npc_form_success(self):
#         """Successfully create an NPC"""
#         form = forms.NPCForm(data=self.form_data)
#         self.assertTrue(form.is_valid())

#     def test_npc_form_bad_name(self):
#         """Fail to create an NPC because of no name"""
#         form_data_test = dict(self.form_data)
#         form_data_test['name'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_npc_form_bad_level(self):
#         """Fail to create an NPC because of no level"""
#         form_data_test = dict(self.form_data)
#         form_data_test['level'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())

#     def test_npc_form_bad_alignment(self):
#         """Fail to create an npc because of no alignment"""
#         form_data_test = dict(self.form_data)
#         form_data_test['alignment'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_size(self):
#         """Fail to create an npc because of no size"""
#         form_data_test = dict(self.form_data)
#         form_data_test['size'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_languages(self):
#         """Fail to create an npc because of no languages"""
#         form_data_test = dict(self.form_data)
#         form_data_test['languages'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_strength(self):
#         """Fail to create an npc because of no strength"""
#         form_data_test = dict(self.form_data)
#         form_data_test['strength'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_dexterity(self):
#         """Fail to create an npc because of no dexterity"""
#         form_data_test = dict(self.form_data)
#         form_data_test['dexterity'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_constitution(self):
#         """Fail to create an npc because of no constitution"""
#         form_data_test = dict(self.form_data)
#         form_data_test['constitution'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_intelligence(self):
#         """Fail to create an npc because of no intelligence"""
#         form_data_test = dict(self.form_data)
#         form_data_test['intelligence'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_wisdom(self):
#         """Fail to create an npc because of no wisdom"""
#         form_data_test = dict(self.form_data)
#         form_data_test['wisdom'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_charisma(self):
#         """Fail to create an npc because of no charisma"""
#         form_data_test = dict(self.form_data)
#         form_data_test['charisma'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_armor_class(self):
#         """Fail to create an npc because of no armor_class"""
#         form_data_test = dict(self.form_data)
#         form_data_test['armor_class'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_hit_points(self):
#         """Fail to create an npc because of no hit_points"""
#         form_data_test = dict(self.form_data)
#         form_data_test['hit_points'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_speed(self):
#         """Fail to create an npc because of no speed"""
#         form_data_test = dict(self.form_data)
#         form_data_test['speed'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_saving_throws(self):
#         """Fail to create an npc because of no saving_throws"""
#         form_data_test = dict(self.form_data)
#         form_data_test['saving_throws'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_skills(self):
#         """Fail to create an npc because of no skills"""
#         form_data_test = dict(self.form_data)
#         form_data_test['skills'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_npc_class(self):
#         """Fail to create an npc because of no npc_class"""
#         form_data_test = dict(self.form_data)
#         form_data_test['npc_class'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_age(self):
#         """Fail to create an npc because of no age"""
#         form_data_test = dict(self.form_data)
#         form_data_test['age'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_height(self):
#         """Fail to create an npc because of no height"""
#         form_data_test = dict(self.form_data)
#         form_data_test['height'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_weight(self):
#         """Fail to create an npc because of no weight"""
#         form_data_test = dict(self.form_data)
#         form_data_test['weight'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_creature_type(self):
#         """Fail to create an npc because of no creature_type"""
#         form_data_test = dict(self.form_data)
#         form_data_test['creature_type'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_damage_vulnerabilities(self):
#         """Fail to create an npc because of no damage_vulnerabilities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['damage_vulnerabilities'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_damage_immunities(self):
#         """Fail to create an npc because of no damage_immunities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['damage_immunities'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_condition_immunities(self):
#         """Fail to create an npc because of no condition_immunities"""
#         form_data_test = dict(self.form_data)
#         form_data_test['condition_immunities'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_senses(self):
#         """Fail to create an npc because of no senses"""
#         form_data_test = dict(self.form_data)
#         form_data_test['senses'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())
        
#     def test_npc_form_bad_challenge_rating(self):
#         """Fail to create an npc because of no challenge_rating"""
#         form_data_test = dict(self.form_data)
#         form_data_test['challenge_rating'] = ''
#         form = forms.NPCForm(data=form_data_test)
#         self.assertFalse(form.is_valid())