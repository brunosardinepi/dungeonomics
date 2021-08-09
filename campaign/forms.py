from django import forms
from django.contrib.auth.models import User

from . import models


class TinyMCEForm(forms.ModelForm):
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

class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'title',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Campaign title'}),
        }

class ChapterForm(TinyMCEForm):
    class Meta:
        model = models.Chapter
        fields = [
            'title',
            'content',
            'order',
        ]

class SectionForm(TinyMCEForm):
    class Meta:
        model = models.Section
        fields = [
            'title',
            'content',
            'order',
        ]

class ImportCampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'title',
        ]

ChapterFormSet = forms.modelformset_factory(
    models.Chapter,
    form=ChapterForm,
    extra=0,
)

ChapterInlineFormSet = forms.inlineformset_factory(
    models.Campaign,
    models.Chapter,
    extra=0,
    fields=('order', 'title'),
    formset=ChapterFormSet,
)

SectionFormSet = forms.modelformset_factory(
    models.Section,
    form=SectionForm,
    extra=0,
)

SectionInlineFormSet = forms.inlineformset_factory(
    models.Chapter,
    models.Section,
    extra=0,
    fields=('order', 'title'),
    formset=SectionFormSet,
)

class CampaignPublishForm(TinyMCEForm):
    class Meta:
        model = models.Campaign
        fields = [
            'tavern_description',
        ]
