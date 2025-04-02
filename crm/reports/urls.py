from django.urls import path
from . import views

urlpatterns = [
    path('contacts_by_category/', views.contacts_by_category_report, name='contacts-by-category-report'),
    path('recent_activities/', views.recent_activities_report, name='recent-activities-report'),
]