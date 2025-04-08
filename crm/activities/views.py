from rest_framework import serializers, viewsets, generics, status
from .models import Activity
from contacts.models import Contact
from .serializers import ActivitySerializer, ActivityWithContactSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ActivityFilter
from .permissions import IsContactRelatedOrReadOnly, IsContactRelatedOrReadOnly, CanAssignActivity, CanExtendDueDate
from rest_framework import filters
from rest_framework.response import Response


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsContactRelatedOrReadOnly, CanAssignActivity, CanExtendDueDate]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ActivityFilter
    search_fields = ['activity_type','subject', ]
    ordering_fields = ['assigned_to__username', 'activity_type', 'subject', 'due_date','priority', 'completed', 'created_at', 'updated_at',
'contact__first_name', 'contact__last_name', 'created_by__username']
    

    def get_queryset(self):
        return Activity.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete() 

class ContactActivitiesListView(generics.ListCreateAPIView):
    serializer_class = ActivityWithContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  
    filterset_fields = ['activity_type', 'subject']
    ordering_fields = ['activity_type', 'due_date', 'completed', 'created_at'] 


    def get_queryset(self):
        contact_id = self.kwargs.get('id')
        return Activity.objects.filter(contact_id=contact_id, is_deleted=False)

    def perform_create(self, serializer): #overriding CreateAPIView's method
        contact_id = self.kwargs.get('id')
        try:
            contact = Contact.objects.get(pk=contact_id) #get this contact with the pk=contact_id
            serializer.save(contact=contact, created_by=self.request.user) #set contact and created_by fields automaticaly with the contact whose activity is viewd 
        except Contact.DoesNotExist:                                       #and the authenticated user respectively        
            raise serializers.ValidationError("Contact not found.")
        

#new feature to show new task
class TaskListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ActivityFilter 
    

    def get_queryset(self):
        return Activity.objects.filter(activity_type='task', is_deleted=False)