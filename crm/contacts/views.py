from rest_framework import viewsets, status
from .models import Contact, Company
from .serializers import ContactSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContactFilter, CompanyFilter
from .permissions import IsAssignedUserOrReadOnly, IsStaffOrReadOnly, IsCompanyAdminOrReadOnly, IsAssignedOrReadOnly, CanAssignContact

from rest_framework import filters 
from rest_framework.response import Response

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'city', 'country', 'created_at', 'updated_at']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete() # This line do hard delete for Company object
    
    

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrReadOnly, CanAssignContact]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContactFilter
    search_fields = ['first_name','last_name','phone_number','created_at']
    ordering_fields = ['first_name', 'last_name', 'category', 'company__name', 'assigned_to__username', 'created_at', 'updated_at']



    def get_queryset(self): #to return only contacts with theit is_deleted fields set to false 
        return Contact.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()