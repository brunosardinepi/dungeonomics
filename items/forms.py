from django import forms
from items import models


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
            'name',
            'item_type',
            'rarity',
            'content',
        ]

class CopyItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name']
