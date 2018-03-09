from django import template
from django.shortcuts import get_object_or_404

from votes.models import Feature, Vote


register = template.Library()

@register.simple_tag
def user_voted(user, feature_pk):
    feature = get_object_or_404(Feature, pk=feature_pk)
    try:
        vote = Vote.objects.get(feature=feature, user=user)
    except Vote.DoesNotExist:
        vote = None

    if vote:
        return True
    else:
        return False