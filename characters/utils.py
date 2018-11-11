from django.shortcuts import get_object_or_404

from . import models


def get_character_object(type, pk):
    if type == 'monster':
        obj = get_object_or_404(models.Monster, pk=pk)
    elif type == 'npc':
        obj = get_object_or_404(models.NPC, pk=pk)
    elif type == 'player':
        obj = get_object_or_404(models.Player, pk=pk)
    return obj

def get_character_types(user):
    # find all of the user's characters
    characters = models.GeneralCharacter.objects.filter(user=user)

    # find all of the "character type" attributes
    types = []
    for character in characters:
        attributes = character.attribute_set.filter(
            name="Character type").values_list('value', flat=True)
        for attribute in attributes:
            types.append(attribute)

    return types
