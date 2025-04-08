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

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='note')
    subject = models.CharField(max_length=255)
    details = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True, help_text="For tasks or scheduled activities")
    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES, default='medium') #Added on april 6
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks') #added on april 6
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity_type}: ({self.contact.first_name} {self.contact.last_name})"
    

    def delete(self, *args, **kwargs): #overriding the defalult delete method to just set is_deleted field to True
        self.is_deleted = True         #for handling soft delet
        self.save()