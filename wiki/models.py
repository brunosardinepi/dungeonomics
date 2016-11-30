from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SectionTemplate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Section(SectionTemplate):
    content = models.TextField(blank=True)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order', 'title', ]

    def get_absolute_url(self):
        return reverse('wiki:home', kwargs={
            'section_pk': self.pk
            })


class Subsection(SectionTemplate):
    content = models.TextField(blank=True)
    order = models.IntegerField(verbose_name= _('Section number'),default=1)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'title',]

    def get_absolute_url(self):
        return reverse('wiki:home', kwargs={
            'section_pk': self.section_id,
            'subsection_pk': self.pk
            })