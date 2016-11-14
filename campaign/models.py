from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CampaignTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Campaign(CampaignTemplate):
    # description = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('campaign:campaign_detail', kwargs={
            'campaign_pk': self.pk
            })


class Chapter(CampaignTemplate):
    content = models.TextField(default='')
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