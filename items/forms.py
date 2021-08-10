from django import forms
from dungeonomics.forms import FormTemplate
from items import models


class ItemForm(FormTemplate):
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
