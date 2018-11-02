from django import forms

from . import models


class TavernReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = [
            'score',
            'comment',
        ]