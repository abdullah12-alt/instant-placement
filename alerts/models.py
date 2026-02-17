from django.db import models
from django.contrib.auth.models import User

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    query = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    remote_only = models.BooleanField(default=False)
    last_sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} in {self.location}"
