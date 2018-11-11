from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )

class ArticleForm(TinyMCEForm):
    class Meta:
        model = models.Article
        fields = [
            'title',
            'tags',
            'description',
        ]
