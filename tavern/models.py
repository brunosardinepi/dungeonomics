from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey('campaign.Campaign',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    monster = models.ForeignKey('characters.Monster',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    npc = models.ForeignKey('characters.NPC',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey('characters.Player',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    character = models.ForeignKey('characters.GeneralCharacter',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(blank=True)
