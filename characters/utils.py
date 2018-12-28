from collections import OrderedDict

from django.shortcuts import get_object_or_404

from .models import Attribute, GeneralCharacter


def get_character_type(character):
    try:
        attribute = Attribute.objects.filter(
            character=character, name="Character type").order_by('pk').first()
    except Attribute.DoesNotExist:
        attribute = None

    return attribute

def get_character_types(user):
    # find all of the user's characters
    characters = GeneralCharacter.objects.filter(user=user)

    # find all of the "character type" attributes
    types = []
    for character in characters:
        attributes = character.attribute_set.filter(
            name="Character type").values_list('value', flat=True)
        if attributes:
            # found type
            for attribute in attributes:
                if attribute not in types:
                    types.append(attribute)
        else:
            # no type specified
            if "Other" not in types:
                types.append("Other")

    # sort alphabetically
    types.sort(key=lambda x: x.lower())

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
        except Attribute.DoesNotExist:
            attribute = None
        stats[stat]['attribute'] = attribute
    return stats

def get_characters(user):
    character_types = get_character_types(user)
    characters = OrderedDict()
    for character_type in character_types:
        # create a dict key for the type and an empty list to hold the characters
        # with the corresponding character type
        characters[character_type] = []

        if character_type == "Other":
            # find all the characters for this user
            # that don't have an attribute named "Character type"
            characters_queryset = GeneralCharacter.objects.filter(
                user=user).exclude(attribute__name="Character type")
            for character in characters_queryset:
                characters[character_type].append(character)
        else:
            # find all the attributes that are named "Character type"
            # then get their associated character and add it to the dict list
            attributes = Attribute.objects.filter(
                character__user=user,
                name="Character type",
                value=character_type,
            ).order_by('character__name')
            for attribute in attributes:
                if attribute.character not in characters[character_type]:
                    characters[character_type].append(attribute.character)

    return characters
