from django import template
from django.utils.safestring import mark_safe
from django.core import serializers

import json

from campaign import models
from campaign.utils import rating_stars_html

register = template.Library()

def jsonify(value):
    '''Convert Django object to JSON object'''
    return serializers.serialize("json", value)

@register.simple_tag
def sections_in_chapter(chapter_pk):
    '''Returns dictionary of sections to display in export'''
    chapter = models.Chapter.objects.get(pk=chapter_pk)
    sections = sorted(models.Section.objects.filter(chapter=chapter),
            key=lambda section: section.order
            )
    if sections:
        for section in sections:
            section.content = json.dumps(section.content)
    return sections

@register.simple_tag
def rating_stars_html_tag(rating):
    return rating_stars_html(rating)

register.filter('jsonify', jsonify)
register.filter('sections_in_chapter', sections_in_chapter)
register.filter('rating_stars_html_tag', rating_stars_html_tag)
