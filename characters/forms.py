from django import forms

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

class CharacterForm(TinyMCEForm):
    class Meta:
        model = models.GeneralCharacter
        fields = [
            'name',
            'notes',
        ]

AttributeFormSet = forms.inlineformset_factory(
    models.GeneralCharacter,
    models.Attribute,
    fields=('name', 'value',),
    extra=2,
    min_num=0,
)

class CharacterPublishForm(TinyMCEForm):
    class Meta:
        model = models.Character
        fields = [
            'tavern_description',
        ]
