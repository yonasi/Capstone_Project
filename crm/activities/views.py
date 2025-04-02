from rest_framework import serializers, viewsets, generics
from .models import Activity
from contacts.models import Contact
from .serializers import ActivitySerializer, ActivityWithContactSerializer
from rest_framework.permissions import IsAuthenticated

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

class ContactActivitiesListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

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