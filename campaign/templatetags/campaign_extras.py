from django import template
from django.utils.safestring import mark_safe
from django.core import serializers

from campaign import models

import json


register = template.Library() 

def jsonify(value): 
    '''Convert Django object to JSON object'''
    # return mark_safe(json.dumps(value))
    return serializers.serialize("json", value)

@register.simple_tag
def sections_in_chapter(chapter_pk):
    '''Returns dictionary of sections to display in export'''
    chapter = models.Chapter.objects.get(pk=chapter_pk)
    # sections = models.Section.objects.filter(chapter=chapter).order_by('order')
    sections = sorted(models.Section.objects.filter(chapter=chapter),
            key=lambda section: section.order
            )
    return {'sections': sections}


register.filter('jsonify', jsonify)
register.filter('sections_in_chapter', sections_in_chapter)