from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.pricing, name='pricing'),
    path('subscribe/apply-promo/', views.apply_promo_code, name='apply_promo_code'),
    path('subscribe/paddle-checkout/', views.paddle_checkout, name='paddle_checkout'),
    path('subscribe/success/', views.paddle_success, name='paddle_success'),
    path('subscribe/cancel/', views.paddle_cancel, name='paddle_cancel'),
    path('paddle/webhook/', views.paddle_webhook, name='paddle_webhook'),
]
