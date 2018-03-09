from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from votes.models import Feature, Vote


class VoteView(View):
    def get(self, request, feature_pk):
        feature = get_object_or_404(Feature, pk=feature_pk)

        # check if the user has voted for this already
        try:
            vote = Vote.objects.get(feature=feature, user=request.user)
        except Vote.DoesNotExist:
            vote = None

        # if the user has already voted for this,
        # delete their vote
        if vote:
            vote.delete()

        # if this is a new vote for this user,
        # register the vote
        # and redirect to the home page
        else:
            Vote.objects.create(
                feature=feature,
                user=request.user,
            )

        return redirect('home')