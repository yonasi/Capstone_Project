from rest_framework import viewsets
from .models import Contact, Company
from .serializers import ContactSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContactFilter, CompanyFilter
from .permissions import IsAssignedUserOrReadOnly, IsStaffOrReadOnly
from rest_framework import filters

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyFilter
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'city', 'country', 'created_at', 'updated_at']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsAssignedUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContactFilter
    search_fields = ['first_name','last_name','phone_number','created_at']
    ordering_fields = ['first_name', 'last_name', 'category', 'company__name',
'assigned_to__username', 'created_at', 'updated_at']