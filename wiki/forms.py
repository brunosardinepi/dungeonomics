from django import forms
from dungeonomics.forms import FormTemplate
from wiki import models


class ArticleForm(FormTemplate):
    class Meta:
        model = models.Article
        fields = [
            'title',
            'tags',
            'description',
        ]
