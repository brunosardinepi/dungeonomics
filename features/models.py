from django.contrib.auth.models import User
from django.db import models


class Feature(models.Model):
    description = models.TextField()
    new = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    @property
    def vote_count(self):
        return self.vote_set.all().count()

    def has_user_vote(self, user):
        try:
            Vote.objects.get(
                user=user,
                feature=self,
            )
            return True
        except Vote.DoesNotExist:
            return False

class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
