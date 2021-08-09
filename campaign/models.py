from characters.models import Monster, NPC, Player
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from tavern.models import Review
import uuid


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

    @property
    def campaign_toolbar(self):
        toolbar = [
            {
                'tooltip': 'Create chapter',
                'url': reverse(
                    'campaign:chapter_create',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-file-plus',
            },
            {
                'tooltip': 'Edit campaign',
                'url': reverse(
                    'campaign:campaign_update',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-edit',
            },
            {
                'tooltip': 'Export campaign',
                'url': reverse(
                    'campaign:campaign_export',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-cloud-download-alt',
            },
            {
                'tooltip': 'Print campaign',
                'url': reverse(
                    'campaign:campaign_print',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-print',
            },
            {
                'tooltip': 'Delete campaign',
                'url': reverse(
                    'campaign:campaign_delete',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-trash-alt',
            },
        ]

        if self.is_published == True:
            toolbar.append(
                {
                    'tooltip': 'View campaign on the Tavern',
                    'url': reverse(
                        'tavern:tavern_campaign_detail',
                        kwargs={'campaign_pk': self.pk},
                    ),
                    'icon': 'fa-beer',
                },
            )
        else:
            toolbar.append(
                {
                    'tooltip': 'Publish campaign to the Tavern',
                    'url': reverse(
                        'campaign:campaign_publish',
                        kwargs={'campaign_pk': self.pk},
                    ),
                    'icon': 'fa-cloud-upload-alt',
                },
            )

        return toolbar

    @property
    def party_toolbar(self):
        toolbar = [
            {
                'tooltip': 'View campaign party',
                'url': reverse(
                    'campaign:campaign_party',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-users',
            },
            {
                'tooltip': 'Create new post',
                'url': reverse(
                    'campaign:post_create',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-comments-alt',
            },
            {
                'tooltip': 'Invite new member to party',
                'url': reverse(
                    'campaign:campaign_party_invite',
                    kwargs={'campaign_pk': self.pk},
                ),
                'icon': 'fa-paper-plane',
            },
        ]

        return toolbar

    def children(self):
        contents = OrderedDict()
        chapters = self.chapter_set.all().order_by('order')
        for chapter in chapters:
            sections = chapter.section_set.all().order_by('order')
            contents[chapter] = sections

        return contents

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

    @property
    def chapter_toolbar(self):
        toolbar = [
            {
                'tooltip': 'Create section',
                'url': reverse(
                    'campaign:section_create',
                    kwargs={
                        'campaign_pk': self.campaign.pk,
                        'chapter_pk': self.pk,
                    },
                ),
                'icon': 'fa-file-plus',
            },
            {
                'tooltip': 'Edit chapter',
                'url': reverse(
                    'campaign:chapter_update',
                    kwargs={
                        'campaign_pk': self.campaign.pk,
                        'chapter_pk': self.pk,
                    },
                ),
                'icon': 'fa-edit',
            },
            {
                'tooltip': 'Delete chapter',
                'url': reverse(
                    'campaign:chapter_delete',
                    kwargs={
                        'campaign_pk': self.campaign.pk,
                        'chapter_pk': self.pk,
                    },
                ),
                'icon': 'fa-trash-alt',
            },
        ]

        return toolbar

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

    @property
    def section_toolbar(self):
        toolbar = [
            {
                'tooltip': 'Edit section',
                'url': reverse(
                    'campaign:section_update',
                    kwargs={
                        'campaign_pk': self.campaign.pk,
                        'chapter_pk': self.chapter.pk,
                        'section_pk': self.pk,
                    },
                ),
                'icon': 'fa-edit',
            },
            {
                'tooltip': 'Delete section',
                'url': reverse(
                    'campaign:section_delete',
                    kwargs={
                        'campaign_pk': self.campaign.pk,
                        'chapter_pk': self.chapter.pk,
                        'section_pk': self.pk,
                    },
                ),
                'icon': 'fa-trash-alt',
            },
        ]

        return toolbar
