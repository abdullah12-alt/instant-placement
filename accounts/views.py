from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import SavedJob

@login_required
def profile(request):
    recent_jobs = SavedJob.objects.filter(user=request.user).order_by('-saved_at')[:3]
    return render(request, 'accounts/profile.html', {'recent_jobs': recent_jobs})
