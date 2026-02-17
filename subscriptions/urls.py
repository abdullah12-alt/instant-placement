from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.pricing, name='pricing'),
    path('subscribe/checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('subscribe/success/', views.stripe_success, name='stripe_success'),
    path('subscribe/cancel/', views.stripe_cancel, name='stripe_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('stripe/manage/', views.stripe_manage, name='stripe_manage'),
]
