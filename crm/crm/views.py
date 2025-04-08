from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

class CustomAPIRoot(APIView):
    permission_classes = [permissions.AllowAny]
    """
    Welcome to the CRM API!

    This API provides endpoints for managing contacts, companies, activities, users and generates basic reports.

    Available endpoints:
    - contacts: Manage contacts.
    - companies: Manage companies.
    - activities: Manage activities (calls, emails, meetings, tasks, notes).
    - users: Manage user accounts (registration, login, profile, logout and password cahanging).
    -reports: Generates basic report data
    """
    def get(self, request, format=None):
        return Response({
            'contacts': reverse('contact-list', request=request, format=format),
            'companies': reverse('company-list', request=request, format=format),
            'activities': reverse('activity-list', request=request, format=format),
            'tasks': reverse('task-list', request=request, format=format),
            'register': reverse('user-register', request=request, format=format),
            'login': reverse('user-login', request=request, format=format),
            'profile': reverse('user-profile', request=request, format=format),
            'profile/update': reverse('profile-update', request=request, format=format),
            'password/change': reverse('password-change', request=request, format=format),
            'logout': reverse('logout', request=request, format=format),
            """Reports"""
            'contacts_by_catagory':reverse('contacts-by-category-report', request=request, format=format),
            'recent_activities': reverse('recent-activities-report', request=request, format=format),
            'sales': reverse('sales-report', request=request, format=format),
            'contacs_created_by_month': reverse('contacts-created-by-month-report', request=request, format=format)
        })