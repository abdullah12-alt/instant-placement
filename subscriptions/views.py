import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from accounts.models import Profile
from django.utils import timezone
from datetime import timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

def pricing(request):
    return render(request, 'subscriptions/pricing.html')

@login_required
def stripe_checkout(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.build_absolute_uri('/subscribe/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/subscribe/cancel/'),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def stripe_success(request):
    profile = request.user.profile
    profile.is_pro = True
    profile.subscription_end_date = timezone.now() + timedelta(days=30)
    profile.save()
    return render(request, 'subscriptions/success.html')

@login_required
def stripe_cancel(request):
    return render(request, 'subscriptions/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=customer_email)
            profile = user.profile
            profile.is_pro = True
            profile.stripe_customer_id = session.get('customer')
            profile.stripe_subscription_id = session.get('subscription')
            profile.subscription_end_date = timezone.now() + timedelta(days=30)
            profile.save()
        except User.DoesNotExist:
            pass
            
    return HttpResponse(status=200)

@login_required
def stripe_manage(request):
    return redirect('profile')
