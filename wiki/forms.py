from django import forms
from wiki import models


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = [
            'title',
            'tags',
            'description',
        ]
