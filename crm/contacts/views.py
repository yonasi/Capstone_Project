from rest_framework import viewsets
from .models import Contact, Company
from .serializers import ContactSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]