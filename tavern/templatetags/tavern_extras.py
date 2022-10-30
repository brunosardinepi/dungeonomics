from django import template

from tavern.utils import rating_stars_html

register = template.Library()

@register.filter
def object_class(obj):
    return obj.__class__.__name__

@register.filter
def tavern_badge_style(obj):
    result = ''

    if object_class(obj).lower() == 'campaign':
        result = "bg-danger"
    elif object_class(obj).lower() == 'player':
        result = "bg-success"
    elif object_class(obj).lower() == 'npc':
        result = "bg-info"
    elif object_class(obj).lower() == 'monster':
        result = "bg-warning"
    else:
        result = "bg-primary"

    return result

@register.simple_tag
def rating_stars_html_tag(rating):
    return rating_stars_html(rating)

register.filter('rating_stars_html_tag', rating_stars_html_tag)

