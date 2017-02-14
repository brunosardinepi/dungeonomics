from django import template
from django.shortcuts import get_object_or_404

from locations import models


register = template.Library()


@register.simple_tag
def get_world_locations(world_pk):
    """
    Return world's locations
    """

    world_locations = models.Location.objects.filter(world=world_pk).exclude(parent_location__isnull=False)
    return world_locations

@register.simple_tag
def get_child_locations(location_pk):
    """
    Return location's children
    """

    child_locations = models.Location.objects.filter(parent_location=location_pk)
    return child_locations


register.filter('get_world_locations', get_world_locations)
register.filter('get_child_locations', get_child_locations)
