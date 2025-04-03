import django_filters
from .models import Contact, Company
from django.conf import settings

class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ChoiceFilter(choices=Contact.CATEGORY_CHOICES)
    company = django_filters.ModelChoiceFilter(queryset=Company.objects.all())
    assigned_to = django_filters.ModelChoiceFilter(queryset=settings.AUTH_USER_MODEL.objects.all())  # optionaly we can  Filter by user ID

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'category', 'company', 'assigned_to']

class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = ['name', 'city', 'country']