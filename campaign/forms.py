from campaign import models
from django import forms
from django.contrib.auth.models import User


#class CreateFormTemplate(forms.ModelForm):
#    # Reference from CampaignCreate
#    def get(self, request, *args, **kwargs):
#        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
#        if campaign.user == request.user:
#            data = at_tagging(request)
#            data['campaign'] = campaign
#            data['form'] = forms.ChapterForm()
#            data['chapter_number'] = utils.get_next_order(campaign)
#            return render(request, 'campaign/chapter_form.html', data)
#        raise Http404

#    def post(self, request, *args, **kwargs):
#        campaign = get_object_or_404(models.Campaign, pk=kwargs['campaign_pk'])
#        if campaign.user == request.user:
#            form = forms.ChapterForm(request.POST)
#            if form.is_valid():
#                chapter = form.save(commit=False)
#                chapter.user = request.user
#                chapter.campaign = campaign
#                chapter.save()
#                messages.add_message(request, messages.SUCCESS, "Chapter created")
#                return HttpResponseRedirect(chapter.get_absolute_url())
#        raise Http404


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'title',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Campaign title'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

class ChapterForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

class SectionForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

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

class CampaignPublishForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = [
            'tavern_description',
        ]
