from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from accounts.models import Profile
from django.utils import timezone
from datetime import timedelta
import hmac
import hashlib
import json

def pricing(request):
    context = {
        'PADDLE_CLIENT_KEY': settings.PADDLE_CLIENT_KEY,
        'PADDLE_PRICE_ID': settings.PADDLE_PRICE_ID,
        'USE_PADDLE_CHECKOUT': getattr(settings, 'USE_PADDLE_CHECKOUT', True),
    }
    return render(request, 'subscriptions/pricing.html', context)

@login_required
def paddle_checkout(request):
    # This might be redundant if we use Paddle.js exclusively on frontend
    return redirect('pricing')

@login_required
def apply_promo_code(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            promo_code = body.get('promo_code', '').strip().upper()
            
            promo_file_path = settings.BASE_DIR / 'promo_codes.json'
            if promo_file_path.exists():
                with open(promo_file_path, 'r') as f:
                    promo_codes = json.load(f)
                    
                if promo_codes.get(promo_code):
                    profile = request.user.profile
                    profile.is_pro = True
                    profile.subscription_end_date = timezone.now() + timedelta(days=365) # 1 year for promo
                    profile.save()
                    return JsonResponse({'success': True, 'message': 'Promo code applied! You are now a Pro user.'})
                
            return JsonResponse({'success': False, 'message': 'Invalid promo code.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)

@login_required
def paddle_success(request):
    # Fallback success page, though webhook should handle official status
    profile = request.user.profile
    profile.is_pro = True
    profile.subscription_end_date = timezone.now() + timedelta(days=30)
    profile.save()
    return render(request, 'subscriptions/success.html')

@login_required
def paddle_cancel(request):
    return render(request, 'subscriptions/cancel.html')

@csrf_exempt
def paddle_webhook(request):
    # Paddle Billing v2 Webhook Logic
    # Verify signature from Header 'Paddle-Signature'
    signature = request.META.get('HTTP_PADDLE_SIGNATURE')
    if not signature:
        return HttpResponse(status=400)
    
    # Paddle v2 uses a more complex signature verification ideally handled by SDK
    # For now, we'll assume basic validation or trust if in dev, 
    # but in production you MUST use paddle-billing SDK or follow 
    # their manual verification guide.
    
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        
        if event_type == 'subscription.created' or event_type == 'subscription.updated':
            subscription = data['data']
            customer_id = subscription.get('customer_id')
            subscription_id = subscription.get('id')
            status = subscription.get('status')
            
            # Find user based on customer_id or custom_data/email
            # Usually you'd store custom_data in the checkout to link user
            from django.contrib.auth.models import User
            # Logic to find user...
            
        elif event_type == 'transaction.completed':
            # Handle payment completion
            pass
            
    except Exception as e:
        return HttpResponse(status=400)
        
    return HttpResponse(status=200)
