from rest_framework import serializers
from .models import Activity
from contacts.serializers import ContactSerializer  
from django.contrib.auth import get_user_model
from contacts.models import Contact

User = get_user_model()
class ActivitySerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Optional: Serializer to show nested contact details in activity list/retrieve
class ActivityWithContactSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']