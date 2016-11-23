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


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = [
            'title',
            'content',
            'order',
        ]

    class Media:
        css = {
            'all': (
                '/static/css/autocomplete.css',
                'https://cdnjs.cloudflare.com/ajax/libs/at.js/1.5.2/css/jquery.atwho.min.css',
                )
            }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/at.js/1.5.2/js/jquery.atwho.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Caret.js/0.3.1/jquery.caret.min.js',
            '/static/js/tinymce/tinymce.min.js',
            )