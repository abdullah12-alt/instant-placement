from django.utils import timezone

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.is_pro and profile.subscription_end_date:
                    if profile.subscription_end_date < timezone.now():
                        profile.is_pro = False
                        profile.save()
            except AttributeError:
                pass
        
        response = self.get_response(request)
        return response
