from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    level = models.IntegerField(default=1)
    ALIGNMENT_CHOICES = (
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
    languages = models.CharField(max_length=255, default='Common')
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    armor_class = models.IntegerField(default=0)
    hit_points = models.IntegerField(default=0)
    speed = models.CharField(max_length=255, default='')
    saving_throws = models.CharField(max_length=255, default='')
    skills = models.CharField(max_length=255, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Monster(Character):
    creature_type = models.CharField(max_length=255, default='')
    damage_vulnerabilities = models.CharField(max_length=255, default='')
    damage_immunities = models.CharField(max_length=255, default='')
    condition_immunities = models.CharField(max_length=255, default='')
    senses = models.CharField(max_length=255, default='')
    challenge_rating = models.IntegerField(default=1)
    traits = models.TextField(blank=True)
    actions = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('characters:monster_detail', kwargs={
            'monster_pk': self.pk
            })


class NPC(Character):
    npc_class = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=1)
    height = models.CharField(max_length=255, default='')
    weight = models.CharField(max_length=255, default='')
    creature_type = models.CharField(max_length=255, default='')
    damage_vulnerabilities = models.CharField(max_length=255, default='')
    damage_immunities = models.CharField(max_length=255, default='')
    condition_immunities = models.CharField(max_length=255, default='')
    senses = models.CharField(max_length=255, default='')
    challenge_rating = models.CharField(max_length=255, default='')
    traits = models.TextField(blank=True)
    actions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'NPC'
        verbose_name_plural = 'NPCs'

    def get_absolute_url(self):
        return reverse('characters:npc_detail', kwargs={
            'npc_pk': self.pk
            })