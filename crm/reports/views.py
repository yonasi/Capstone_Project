from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from contacts.models import Contact
from activities.models import Activity
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncMonth

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contacts_by_category_report(request):
    contacts_by_category = Contact.objects.values('category').annotate(count=Count('id'))
    report_data = {}
    for item in contacts_by_category:
        report_data[item['category']] = item['count']
    return Response(report_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activities_report(request):
    limit = request.query_params.get('limit', 8)  # Default to 8 recent activities
    try:
        limit = int(limit)
    except ValueError:
        return Response({'error': 'Invalid limit parameter'}, status=status.HTTP_400_BAD_REQUEST)

    recent_activities = Activity.objects.order_by('-created_at')[:limit]

    from activities.serializers import ActivityWithContactSerializer  
    serializer = ActivityWithContactSerializer(recent_activities, many=True)
    return Response(serializer.data)

#new features created on april 6
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_report(request):
    sales_data = Contact.objects.values('category').annotate(count=Count('id')).order_by('category')
    report_data = {}

    for item in sales_data:
        report_data[item['category']] = item['count']
    return Response(report_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contacts_created_by_month_report(request):
    
    year = request.query_params.get('year')
    contacts = Contact.objects.annotate(month=TruncMonth('created_at'))
    if year:
        try:
            year = int(year)
            contacts = contacts.filter(created_at__year=year)
        except ValueError:
            return Response({'error': 'Invalid year parameter'}, status=status.HTTP_400_BAD_REQUEST)

    contacts_by_month = contacts.values('month').annotate(count=Count('id')).order_by('month')
    report_data = {}
    for item in contacts_by_month:
        report_data[item['month'].strftime('%Y-%m')] = item['count']
    return Response(report_data)