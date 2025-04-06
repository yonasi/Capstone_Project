from django.urls import path
from . import views

urlpatterns = [
    path('contacts_by_category/', views.contacts_by_category_report, name='contacts-by-category-report'),
    path('recent_activities/', views.recent_activities_report, name='recent-activities-report'),
     path('sales_funnel/', views.sales_report, name='sales-funnel-report'), #created on april 6
    path('contacts_created_by_month/', views.contacts_created_by_month_report, name='contacts-created-by-month-report'), #created on april 6
]