from django.db import models
from django.conf import settings
from django.utils import timezone
from contacts.models import Contact

class Activity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('task', 'Task'),
        ('note', 'Note'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='note')
    subject = models.CharField(max_length=255)
    details = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True, help_text="For tasks or scheduled activities")
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity_type}: {self.subject} ({self.contact.first_name} {self.contact.last_name})"