import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _

from characters.models import Monster, NPC, Player


class CampaignTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def rating(self):
        # return the average of this campaign's review scores, or 0 if there are no reviews
        return Review.objects.filter(
            campaign=self).aggregate(Avg('score'))['score__avg'] or 0


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

class Campaign(CampaignTemplate):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    public_url = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    tavern_description = models.TextField(blank=True)
    importers = models.ManyToManyField(User, related_name='importers')

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={
            'campaign_pk': self.pk
            })

    def players(self):
        return self.player_set.all().order_by('character_name')

    def rating(self):
        # find the average rating for this campaign
        return Review.objects.filter(
            campaign=self).aggregate(
            Avg('score'))['score__avg'] or 0.00


class Chapter(CampaignTemplate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    order = models.IntegerField(verbose_name= _('Chapter number'),default=1)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'title', ]

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={
            'campaign_pk': self.campaign_id,
            'chapter_pk': self.pk
            })


class Section(CampaignTemplate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    order = models.IntegerField(verbose_name= _('Section number'),default=1)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'title',]

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={
            'campaign_pk': self.campaign_id,
            'chapter_pk': self.chapter_id,
            'section_pk': self.pk
            })


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, blank=True, on_delete=models.CASCADE)
    monster = models.ForeignKey(Monster,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    npc = models.ForeignKey(NPC,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(Player,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(blank=True)