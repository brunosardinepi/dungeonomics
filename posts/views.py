from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from . import forms
from campaign.models import Campaign
from campaign.utils import has_campaign_access


class PostCreate(View):
    def get(self, request, campaign_pk):
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if has_campaign_access(request.user, campaign_pk):
            form = forms.PostForm()
            return render(self.request, 'campaign/campaign_party_post_create.html', {
                'campaign': campaign,
                'form': form,
            })
        else:
            raise Http404

    def post(self, request, campaign_pk):
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if has_campaign_access(request.user, campaign_pk):
            form = forms.PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.campaign = campaign
                post.save()
                messages.add_message(request, messages.SUCCESS, "Post created!")
                return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404