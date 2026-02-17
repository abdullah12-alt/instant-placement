from django.urls import path
from . import views

urlpatterns = [
    path('', views.alerts_list, name='alerts'),
    path('save-ajax/', views.save_search_ajax, name='save_search_ajax'),
    path('delete/<int:pk>/', views.delete_search, name='delete_search'),
]
