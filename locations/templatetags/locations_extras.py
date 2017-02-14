from django import template
from django.shortcuts import get_object_or_404

from locations import models


register = template.Library()


@register.simple_tag
def get_child_locations(location_pk):
    """
    Return location's children
    """

    #location = get_object_or_404(models.Location, pk=location_pk)
    child_locations = models.Location.objects.filter(parent=location_pk)
    return child_locations


register.filter('get_child_locations', get_child_locations)
