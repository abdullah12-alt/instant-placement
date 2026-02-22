from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.search_results, name='search_results'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('save-ajax/', views.save_job_ajax, name='save_job_ajax'),
    path('remove-ajax/', views.remove_job_ajax, name='remove_job_ajax'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
]
