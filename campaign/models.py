import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _


class CampaignTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def rating(self):
        # return the average of this campaign's review scores, or 0 if there are no reviews
        return Review.objects.filter(campaign=self).aggregate(Avg('score'))['score__avg'] or 0


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

class Campaign(CampaignTemplate):
    public_url = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True, blank=True)
    tavern_description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={
            'campaign_pk': self.pk
            })

    def players(self):
        return self.player_set.all().order_by('character_name')


class Chapter(CampaignTemplate):
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
    # content = models.TextField(default='')
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
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=5)
    comment = models.TextField(blank=True)