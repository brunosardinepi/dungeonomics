from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )


class ItemForm(TinyMCEForm):
    class Meta:
        model = models.Item
        fields = [
            'name',
            'item_type',
            'rarity',
            'description',
        ]


class DeleteItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name']


class CopyItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name']