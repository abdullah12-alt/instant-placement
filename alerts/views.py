from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SavedSearch
import json

@login_required
def alerts_list(request):
    if not request.user.profile.is_pro:
        return redirect('pricing')
    searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'alerts/alerts_list.html', {'searches': searches})

@login_required
def save_search_ajax(request):
    if not request.user.profile.is_pro:
        return JsonResponse({'status': 'error', 'message': 'Upgrade to Pro to save searches!'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        if SavedSearch.objects.filter(user=request.user).count() >= 5:
             return JsonResponse({'status': 'error', 'message': 'Limit of 5 saved searches reached.'})
             
        search, created = SavedSearch.objects.get_or_create(
            user=request.user,
            query=data['query'],
            location=data['location'],
            defaults={
                'keywords': data.get('keywords'),
                'remote_only': data.get('remote_only', False)
            }
        )
        if created:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Search already saved.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@login_required
def delete_search(request, pk):
    search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    search.delete()
    return redirect('profile')
