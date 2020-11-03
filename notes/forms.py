from django import forms

from .models import Note
from campaign.models import Campaign


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

class NoteForm(TinyMCEForm):
    class Meta:
        model = Note
        fields = [
            'name',
            'campaign',
            'is_public',
            'content',
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campaign'].queryset = Campaign.objects.filter(
            user=user,
        )

class CopyNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['name']
