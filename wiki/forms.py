from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )


class SectionForm(TinyMCEForm):
    class Meta:
        model = models.Section
        fields = [
            'title',
            'content',
            'order',
        ]


class SubsectionForm(TinyMCEForm):
    class Meta:
        model = models.Subsection
        fields = [
            'title',
            'content',
            'order',
        ]