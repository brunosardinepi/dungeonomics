from campaign import models
from django import forms
from django.contrib.auth.models import User


class FormTemplate(forms.ModelForm):
    class Meta:
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

class CampaignForm(FormTemplate):
    class Meta(FormTemplate.Meta):
        model = models.Campaign
        fields = FormTemplate.Meta.fields

class ChapterForm(FormTemplate):
    class Meta(FormTemplate.Meta):
        model = models.Chapter
        fields = FormTemplate.Meta.fields + [
            'content',
            'order',
        ]

class SectionForm(FormTemplate):
    class Meta(FormTemplate.Meta):
        model = models.Section
        fields = FormTemplate.Meta.fields + [
            'content',
            'order',
        ]

class ImportCampaignForm(forms.ModelForm):
    class Meta(FormTemplate.Meta):
        model = models.Campaign
        fields = [
            'public_url',
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

class CampaignPublishForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'tavern_description',
        ]
