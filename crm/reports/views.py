from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from contacts.models import Contact
from activities.models import Activity
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils import timezone

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
    limit = request.query_params.get('limit', 10)  # Default to 10 recent activities
    try:
        limit = int(limit)
    except ValueError:
        return Response({'error': 'Invalid limit parameter'}, status=status.HTTP_400_BAD_REQUEST)

    recent_activities = Activity.objects.order_by('-created_at')[:limit]
    from activities.serializers import ActivityWithContactSerializer  # Import here to avoid circular dependency
    serializer = ActivityWithContactSerializer(recent_activities, many=True)
    return Response(serializer.data)