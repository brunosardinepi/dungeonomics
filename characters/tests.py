# from django.test import TestCase

# from . import forms


# class MonsterTestCase(TestCase):
#     def test_monster_form_success(self):
#         """Successfully create a monster"""
#         form_data = {
#             'name': 'Sir Bearington',
#             'level': 20,
#             }
#         form = forms.MonsterForm(data=form_data)
#         self.assertTrue(form.is_valid())

#     def test_monster_form_bad_name_1(self):
#         """Fail to create a monster because of no name"""
#         form_data = {
#             'name': '',
#             'level': 20,
#             }
#         form = forms.MonsterForm(data=form_data)
#         self.assertFalse(form.is_valid())

#     def test_monster_form_bad_name_2(self):
#         """Fail to create a monster because of no level"""
#         form_data = {
#             'name': 'Sir Bearington',
#             'level': '',
#             }
#         form = forms.MonsterForm(data=form_data)
#         self.assertFalse(form.is_valid())


# class NPCTestCase(TestCase):
#     def test_npc_form_success(self):
#         """Successfully create an NPC"""
#         form_data = {
#             'name': 'Deckard Cain',
#             'level': 20,
#             }
#         form = forms.NPCForm(data=form_data)
#         self.assertTrue(form.is_valid())

#     def test_npc_form_bad_name_1(self):
#         """Fail to create an NPC because of no name"""
#         form_data = {
#             'name': '',
#             'level': 20,
#             }
#         form = forms.NPCForm(data=form_data)
#         self.assertFalse(form.is_valid())

#     def test_npc_form_bad_name_2(self):
#         """Fail to create an NPC because of no level"""
#         form_data = {
#             'name': 'Sir Bearington',
#             'level': '',
#             }
#         form = forms.NPCForm(data=form_data)
#         self.assertFalse(form.is_valid())