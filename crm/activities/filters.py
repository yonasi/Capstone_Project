import django_filters
from .models import Activity


class ActivityFilter(django_filters.FilterSet):
    activity_type = django_filters.ChoiceFilter(choices=Activity.ACTIVITY_TYPE_CHOICES)
    subject = django_filters.CharFilter(lookup_expr='icontains')
    contact = django_filters.CharFilter(field_name='contact__first_name', lookup_expr='icontains')
    created_by = django_filters.CharFilter(field_name='created_by__username', lookup_expr='icontains')
    due_date__gte = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date__lte = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    completed = django_filters.BooleanFilter()

    class meta:
        model = Activity
        fields = ['priority', 'activity_type', 'subject', 'contact', 'assigned_to', 'created_by', 'due_date__gte', 'due_date__lte', 'completed']