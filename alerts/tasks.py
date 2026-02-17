from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import SavedSearch
from jobs.services import JobService

@shared_task
def send_daily_job_alerts():
    searches = SavedSearch.objects.filter(user__profile__is_pro=True)
    
    for search in searches:
        jobs = JobService.search_jobs(
            query=search.query,
            location=search.location,
            date_posted='today',
            remote_only=search.remote_only,
            user_is_pro=True
        )
        
        if jobs:
            subject = "⚡ Your Daily Jobs Digest — Instant Placement"
            html_content = render_to_string('emails/daily_digest.html', {
                'user': search.user,
                'jobs': jobs[:5],
                'search': search
            })
            text_content = f"Hi {search.user.username}, we found new jobs for your search: {search.query}"
            
            msg = EmailMultiAlternatives(
                subject, text_content, 
                settings.DEFAULT_FROM_EMAIL, [search.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            search.last_sent_at = timezone.now()
            search.save()
