from django import forms
from django.contrib.auth.models import User
from locations import models


class WorldForm(forms.ModelForm):
    class Meta:
        model = models.World
        fields = [
            'name',
            'image',
            'content',
        ]

class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = [
            'name',
            'world',
            'parent_location',
            'image',
            'content',
        ]

    def __init__(self, user_pk, world_pk, location_pk, *args, **kwargs):
        super (LocationForm, self).__init__(*args, **kwargs)
        self.fields['world'].queryset = models.World.objects.filter(user=user_pk)
        self.fields['parent_location'].queryset = models.Location.objects.filter(world=world_pk)

LocationFormSet = forms.modelformset_factory(
    models.Location,
    form=LocationForm,
    extra=0,
)

LocationInlineFormSet = forms.inlineformset_factory(
    models.World,
    models.Location,
    extra=0,
    fields=('name',),
    formset=LocationFormSet,
)
