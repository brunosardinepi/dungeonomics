from collections import OrderedDict

from django.shortcuts import get_object_or_404

from . import models


def get_character_types(user):
    # find all of the user's characters
    characters = models.GeneralCharacter.objects.filter(user=user)

    # find all of the "character type" attributes
    types = []
    for character in characters:
        attributes = character.attribute_set.filter(
            name="Character type").values_list('value', flat=True)
        if attributes:
            # found type
            for attribute in attributes:
                types.append(attribute)
        else:
            # no type specified
            types.append("Other")

    return types

def create_character_copy(character, user):
    # copy the character and its attributes
    # set the owner to the user
    attributes = character.attribute_set.all()
    character.pk = None
    character.is_published = False
    character.user = user
    character.save()
    for attribute in attributes:
        attribute.pk = None
        attribute.save()
        attribute.character = character
        attribute.save()

def get_character_stats(character):
    stats = OrderedDict([
        ("Strength", {"title": "STR", "attribute": None}),
        ("Dexterity", {"title": "DEX", "attribute": None}),
        ("Constitution", {"title": "CON", "attribute": None}),
        ("Intelligence", {"title": "INT", "attribute": None}),
        ("Wisdom", {"title": "WIS", "attribute": None}),
        ("Charisma", {"title": "CHA", "attribute": None}),
    ])
    for stat, attribute in stats.items():
        try:
            attribute = character.attribute_set.get(name=stat)
        except models.Attribute.DoesNotExist:
            attribute = None
        stats[stat]['attribute'] = attribute
    return stats
