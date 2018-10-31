from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    views = models.IntegerField(default=1)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='tags')
    admins = models.ManyToManyField(User, related_name='admins')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article_detail', kwargs={'pk': self.pk})
