from django.db import models
from django.contrib.auth.models import User

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=1000)
    platform = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.CharField(max_length=100, blank=True, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job_id')

    def __str__(self):
        return f"{self.title} at {self.company}"
