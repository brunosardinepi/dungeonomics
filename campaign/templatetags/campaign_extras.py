from django import template
from django.utils.safestring import mark_safe
from django.core import serializers

import json


register = template.Library() 

def jsonify(value): 
    '''Convert Django object to JSON object'''
    return serializers.serialize("json", value)

def int_to_roman(input):
   if type(input) != int:
      raise TypeError("Input must be an integer")
   if not 0 < input < 4000:
      raise ValueError("Input must be between 1 and 3999")
   ints = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
   nums = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result

def int_to_letter(input):
   if type(input) != int:
      raise TypeError("Input must be an integer")
   if not 0 < input < 4000:
      raise ValueError("Input must be between 1 and 3999")
   ints = list(range(1,27))
   letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
   result = ""
   if input <= 26:
      result = letters[(input % 26) - 1]
   if input > 26:
      while input > 26:
         result += 'a'
         input -= 26
      result += letters[(input % 26) - 1]
   return result

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

register.filter('jsonify', jsonify)
register.filter('int_to_roman', int_to_roman)
register.filter('int_to_letter', int_to_letter)
register.filter('sections_in_chapter', sections_in_chapter)
