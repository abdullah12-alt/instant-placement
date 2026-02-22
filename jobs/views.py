from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import JobService
from .models import SavedJob
import json

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

def home(request):
    return render(request, 'jobs/home.html')

def search_results(request):
    query = request.GET.get('q', '')
    location = request.GET.get('l', '')
    keywords = request.GET.get('k', '')
    time_filter = request.GET.get('t', 'today')
    remote_only = request.GET.get('remote') == 'true'
    
    user_is_pro = request.user.is_authenticated and request.user.profile.is_pro
    
    # Restrict pro filters for free users
    if time_filter in ['1h', '8h'] and not user_is_pro:
        time_filter = 'today'
    if remote_only and not user_is_pro:
        remote_only = False

    jobs = JobService.search_jobs(
        query=query,
        location=location,
        date_posted=time_filter,
        remote_only=remote_only,
        num_pages=1,
        user_is_pro=user_is_pro
    )

    # Simple keyword exclusion (Pro feature)
    if user_is_pro and keywords:
        exclude_list = [k.strip().lower() for k in keywords.split(',')]
        jobs = [j for j in jobs if not any(ex in j['job_title'].lower() for ex in exclude_list)]

    context = {
        'jobs': jobs,
        'query': query,
        'location': location,
        'query_k': keywords,
        'query_t': time_filter,
        'query_remote': remote_only,
        't_today': time_filter == 'today',
        't_week': time_filter == 'week',
        't_month': time_filter == 'month',
        't_1h': time_filter == '1h',
        't_8h': time_filter == '8h',
    }
    return render(request, 'jobs/results.html', context)

@login_required
def saved_jobs(request):
    jobs = SavedJob.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'jobs/saved_jobs.html', {'jobs': jobs})

@login_required
def save_job_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Check limit for free users
        if not request.user.profile.is_pro:
            if SavedJob.objects.filter(user=request.user).count() >= 5:
                return JsonResponse({'status': 'error', 'message': 'Free tier limited to 5 saved jobs. Upgrade to Pro for unlimited!'})
        
        job, created = SavedJob.objects.get_or_create(
            user=request.user,
            job_id=data['job_id'],
            defaults={
                'title': data['title'],
                'company': data.get('company'),
                'location': data.get('location'),
                'url': data['url'],
                'platform': data.get('platform')
            }
        )
        if created:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Job already saved.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
def remove_job_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_id = data.get('job_id')
        try:
            job = SavedJob.objects.get(user=request.user, job_id=job_id)
            job.delete()
            return JsonResponse({'status': 'success'})
        except SavedJob.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Job not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
