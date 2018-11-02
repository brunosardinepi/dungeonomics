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
