from campaign import models
from django import forms
from django.contrib.auth.models import User
from dungeonomics.forms import FormTemplate


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'title',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Campaign title'}),
        }

class ChapterForm(FormTemplate):
    class Meta:
        model = models.Chapter
        fields = [
            'title',
            'content',
            'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Chapter title'}),
        }

class SectionForm(FormTemplate):
    class Meta:
        model = models.Section
        fields = [
            'title',
            'content',
            'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Section title'}),
        }

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

class CampaignPublishForm(FormTemplate):
    class Meta:
        model = models.Campaign
        fields = [
            'tavern_description',
        ]
