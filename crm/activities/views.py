from rest_framework import serializers, viewsets, generics
from .models import Activity
from contacts.models import Contact
from .serializers import ActivitySerializer, ActivityWithContactSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ActivityFilter
from .permissions import IsContactRelatedOrReadOnly
from rest_framework import filters


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsContactRelatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ActivityFilter
    search_fields = ['activity_type','subject', ]
    ordering_fields = ['activity_type', 'subject', 'due_date', 'completed', 'created_at', 'updated_at',
'contact__first_name', 'contact__last_name', 'created_by__username']
    
class ContactActivitiesListView(generics.ListCreateAPIView):
    serializer_class = ActivityWithContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    filterset_fields = ['activity_type', 'subject']
    ordering_fields = ['activity_type', 'due_date', 'completed', 'created_at'] 

    def get_queryset(self):
        contact_id = self.kwargs.get('id')
        return Activity.objects.filter(contact_id=contact_id)

    def perform_create(self, serializer):
        contact_id = self.kwargs.get('id')
        try:
            contact = Contact.objects.get(pk=contact_id)
            serializer.save(contact=contact, created_by=self.request.user)
        except Contact.DoesNotExist:
            raise serializers.ValidationError("Contact not found.")