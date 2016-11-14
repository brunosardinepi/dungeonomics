from django import forms

from . import models


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'title',
        ]


class ChapterForm(forms.ModelForm):
    class Meta:
        model = models.Chapter
        fields = [
            'content',
            'order',
        ]