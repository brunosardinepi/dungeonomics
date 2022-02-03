from collections import OrderedDict
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from dungeonomicsdrf import environ
import re
#from tavern.models import Review
import uuid


class CampaignTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def mention(self):
        return f"[{self.__str__()}]({environ.secrets['site']}{self.get_absolute_url()})"

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
    importers = models.ManyToManyField(User, related_name='importers', blank=True)

    class Meta:
        ordering = ['title']

    def rating(self):
        """
        Return the average of this campaign's review scores, or 0 if there are no reviews.
        """
        return self.review_set.objects.aggregate(Avg('score'))['score__avg'] or 0

    def get_absolute_url(self):
        return reverse(
            'campaign:campaign_detail',
            kwargs={'campaign_pk': self.pk},
        )

    def get_tavern_url(self):
        return reverse(
            'tavern:tavern_campaign_detail',
            kwargs={'uuid': self.public_url},
        )

    @property
    def children(self):
        contents = OrderedDict()
        chapters = self.chapter_set.all().order_by('order')
        for chapter in chapters:
            sections = chapter.section_set.all().order_by('order')
            contents[chapter] = sections

        return contents

    @property
    def mentions(self):
        app_labels = {
            'characters': re.compile(
                r'\(http(?:s)?:\/\/(?:garrett)?\.?dungeonomics\.com(?::8000)?(?:\/characters\/)?(?:monster\/\d\/)?(?:player\/\d\/)?(?:npc\/\d\/)?\)',
                flags=re.IGNORECASE,
            ),
            'items': re.compile(
                r'\(http(?:s)?:\/\/(?:garrett)?\.?dungeonomics\.com(?::8000)?(?:\/items\/\d\/)?\)',
                flags=re.IGNORECASE,
            ),
            'locations': re.compile(
                r'\(http(?:s)?:\/\/(?:garrett)?\.?dungeonomics\.com(?::8000)?(?:\/locations\/)?(?:world\/\d\/)?(?:location\/\d\/)?\)',
                flags=re.IGNORECASE,
            ),
            'tables': re.compile(
                r'\(http(?:s)?:\/\/(?:garrett)?\.?dungeonomics\.com(?::8000)?(?:\/tables\/\d\/)?\)',
                flags=re.IGNORECASE,
            ),
        }
        results = {}
        for app_label, regex in app_labels.items():
            for chapter, sections in self.children.items():
                # Look for the dungeonomics URL in the content.
                children = [chapter]
                children += [i for i in sections]
                for child in children:
                    matches = re.findall(
                        regex,
                        child.content,
                    )
                    if matches:
                        matches = [i.lstrip("(").rstrip(")") for i in matches]
                        for match in matches:
                            # Get the object.
                            if app_label in ['characters', 'locations']:
                                match = match.split(f"/{app_label}/")[1]
                                model_name = match.split("/")[0].replace("/", "").strip()
                                pk = match.split("/")[1].replace("/", "").strip()
                            else:
                                model_name = app_label[:-1]
                                pk = match.split(f"/{app_label}/")[1].replace("/", "").strip()

                            model = apps.get_model(
                                app_label=app_label,
                                model_name=model_name,
                            )

                            try:
                                obj = model.objects.get(pk=pk)
                            except model.DoesNotExist:
                                continue

                            # Check if this object already exists in our results.
                            if obj not in results:
                                results[obj] = []
                            results[obj].append(child)

        return results

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
