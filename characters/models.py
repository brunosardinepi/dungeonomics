from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from math import floor


def score_to_mod_string(score):
    return "{:+d}".format(floor((score - 10) / 2))


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    level = models.IntegerField(default=1)
    ALIGNMENT_CHOICES = (
        ('Unaligned', 'Unaligned'),
        ('LG', 'Lawful Good'),
        ('NG', 'Neutral Good'),
        ('CG', 'Chaotic Good'),
        ('LN', 'Lawful Neutral'),
        ('N', 'Neutral'),
        ('CN', 'Chaotic Neutral'),
        ('LE', 'Lawful Evil'),
        ('NE', 'Neutral Evil'),
        ('CE', 'Chaotic Evil'),
    )
    alignment = models.CharField(
        max_length=255,
        choices=ALIGNMENT_CHOICES,
        default='Neutral',
    )
    SIZE_CHOICES = (
        ('Tiny', 'Tiny'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Huge', 'Huge'),
        ('Gargantuan', 'Gargantuan'),
    )
    size = models.CharField(
        max_length=255,
        choices=SIZE_CHOICES,
        default='Medium',
    )
    languages = models.CharField(max_length=255, blank=True)
    strength = models.IntegerField(default=10, blank=True)
    dexterity = models.IntegerField(default=10, blank=True)
    constitution = models.IntegerField(default=10, blank=True)
    intelligence = models.IntegerField(default=10, blank=True)
    wisdom = models.IntegerField(default=10, blank=True)
    charisma = models.IntegerField(default=10, blank=True)
    armor_class = models.CharField(max_length=255, blank=True)
    hit_points = models.CharField(max_length=255, blank=True)
    speed = models.CharField(max_length=255, default='', blank=True)
    saving_throws = models.CharField(max_length=255, default='', blank=True)
    skills = models.CharField(max_length=255, default='', blank=True)

    @property
    def strength_mod(self):
        return score_to_mod_string(self.strength)

    @property
    def dexterity_mod(self):
        return score_to_mod_string(self.dexterity)

    @property
    def constitution_mod(self):
        return score_to_mod_string(self.constitution)

    @property
    def intelligence_mod(self):
        return score_to_mod_string(self.intelligence)

    @property
    def wisdom_mod(self):
        return score_to_mod_string(self.wisdom)

    @property
    def charisma_mod(self):
        return score_to_mod_string(self.charisma)

    class Meta:
        abstract = True


class Monster(Character):
    creature_type = models.CharField(max_length=255, default='', blank=True)
    damage_vulnerabilities = models.CharField(max_length=255, default='', blank=True)
    damage_immunities = models.CharField(max_length=255, default='', blank=True)
    damage_resistances = models.CharField(max_length=255, default='', blank=True)
    condition_immunities = models.CharField(max_length=255, default='', blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    challenge_rating = models.CharField(max_length=255, default='', blank=True)
    content = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('characters:monster_detail', kwargs={
            'monster_pk': self.pk
            })

    def __str__(self):
        return self.name


class NPC(Character):
    npc_class = models.CharField(verbose_name= _('Class'),max_length=255, default='', blank=True)
    race = models.CharField(max_length=255, default='', blank=True)
    age = models.CharField(max_length=255, default='', blank=True)
    height = models.CharField(max_length=255, default='', blank=True)
    weight = models.CharField(max_length=255, default='', blank=True)
    creature_type = models.CharField(max_length=255, default='', blank=True)
    damage_vulnerabilities = models.CharField(max_length=255, default='', blank=True)
    damage_immunities = models.CharField(max_length=255, default='', blank=True)
    damage_resistances = models.CharField(max_length=255, default='', blank=True)
    condition_immunities = models.CharField(max_length=255, default='', blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    challenge_rating = models.CharField(max_length=255, default='', blank=True)
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCs'

    def get_absolute_url(self):
        return reverse('characters:npc_detail', kwargs={
            'npc_pk': self.pk
            })

    def __str__(self):
        return self.name


class Player(Character):
    campaigns = models.ManyToManyField('campaign.Campaign')
    character_name = models.CharField(max_length=255, default='')
    proficiency_bonus = models.CharField(max_length=255, default='', blank=True)
    player_name = models.CharField(max_length=255, default='', blank=True)
    character_class = models.CharField(max_length=255, default='', blank=True)
    race = models.CharField(max_length=255, default='', blank=True)
    xp = models.IntegerField(verbose_name= _('XP'), default=0, blank=True, null=True)
    background = models.CharField(max_length=255, default='', blank=True)
    age = models.CharField(max_length=255, default='', blank=True)
    height = models.CharField(max_length=255, default='', blank=True)
    weight = models.CharField(max_length=255, default='', blank=True)
    initiative = models.CharField(max_length=255, default='', blank=True)
    personality = models.TextField(blank=True)
    bonds = models.TextField(blank=True)
    ideals = models.TextField(blank=True)
    flaws = models.TextField(blank=True)
    feats = models.TextField(blank=True)
    attacks = models.TextField(blank=True)
    spells = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    traits = models.TextField(blank=True)
    proficiencies = models.TextField(blank=True)
    senses = models.CharField(max_length=255, default='', blank=True)
    equipment = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('characters:player_detail', kwargs={
            'player_pk': self.pk
            })

    def __str__(self):
        return self.character_name


class GeneralCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('characters:character_detail', kwargs={'pk': self.pk})

class Attribute(models.Model):
    character = models.ForeignKey(GeneralCharacter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    value = models.CharField(max_length=255, default='')

    def __str__(self):
        return "{}: {}".format(self.character, self.name[:10])

    def get_absolute_url(self):
        return reverse('characters:character_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
