from django import template

from tavern.utils import rating_stars_html

register = template.Library()

@register.simple_tag
def rating_stars_html_tag(rating):
    return rating_stars_html(rating)

register.filter('rating_stars_html_tag', rating_stars_html_tag)
