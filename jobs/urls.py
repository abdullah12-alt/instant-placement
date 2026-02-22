from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.search_results, name='search_results'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('save-ajax/', views.save_job_ajax, name='save_job_ajax'),
]
