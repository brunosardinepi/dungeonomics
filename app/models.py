from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from dungeonomicsdrf import environ
import uuid


class PasswordReset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    email = models.EmailField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        reverse_url = reverse('app:password_reset_action', kwargs={'uuid': self.uuid})
        print(f"reverse_url = {reverse_url}")
        return (
            f"{environ.secrets['protocol']}://"
            f"{environ.secrets['domain']}"
            f"{reverse_url}"
        )
