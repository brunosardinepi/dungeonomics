from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from . import forms
from . import models
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
                messages.success(request, 'Post created!', fail_silently=True)
                return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404

class PostDelete(View):
    def get(self, request, campaign_pk, post_pk):
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if campaign.user == request.user:
            post = get_object_or_404(models.Post, pk=post_pk)
            post.delete()
            messages.success(request, 'Post deleted!', fail_silently=True)
            return redirect('campaign:campaign_party', campaign_pk=campaign.pk)
        else:
            raise Http404


class PostDetail(View):
    def get(self, request, campaign_pk, post_pk):
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if has_campaign_access(request.user, campaign_pk):
            post = get_object_or_404(models.Post, pk=post_pk)
            form = forms.CommentForm()
            return render(self.request, 'campaign/campaign_party_post.html', {
                'campaign': campaign,
                'post': post,
                'form': form,
            })
        else:
            raise Http404

    def post(self, request, campaign_pk, post_pk):
        campaign = get_object_or_404(Campaign, pk=campaign_pk)
        if has_campaign_access(request.user, campaign_pk):
            post = get_object_or_404(models.Post, pk=post_pk)
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                messages.success(request, 'Comment added!', fail_silently=True)
                return redirect('campaign:post_detail', campaign_pk=campaign.pk, post_pk=post.pk)
        else:
            raise Http404