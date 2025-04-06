from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Activity
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings


reminder = Signal()

@receiver(post_save, sender=Activity)
def send_reminder_on_save(sender, instance, created, **kwargs):
    
    if instance.activity_type == 'task':
        reminder.send(sender=sender, activity=instance)

@receiver(reminder)
def process_reminder(sender, activity, **kwargs):
     if activity.due_date and not activity.completed and activity.assigned_to and activity.assigned_to.email:
        now = timezone.now()
        time_until_due = activity.due_date - now

        subject = f"Task Reminder: '{activity.subject}'"
        message = f"Hi {activity.assigned_to.first_name},\n\n"

        if time_until_due <= timezone.timedelta(hours=24) and time_until_due > timezone.timedelta(seconds=0):
            message += f"This is a reminder that the task '{activity.subject}' related to {activity.contact} is due in less than 24 hours, specifically on {activity.due_date.strftime('%Y-%m-%d %H:%M:%S %Z%z')}.\n\n"
        elif time_until_due <= timezone.timedelta(seconds=0) and not activity.completed:
            subject = f"Overdue Task: '{activity.subject}'"
            message += f"This is a notification that the task '{activity.subject}' related to {activity.contact} was due on {activity.due_date.strftime('%Y-%m-%d %H:%M:%S %Z%z')} and is still marked as incomplete.\n\n"
        else:
            return  

        message += f"Task Details:\n"
        message += f"- Subject: {activity.subject}\n"
        message += f"- Details: {activity.details}\n"
        message += f"- Due Date: {activity.due_date.strftime('%Y-%m-%d %H:%M:%S %Z%z')}\n"
        message += f"- Priority: {activity.priority}\n"
        message += f"- Contact: {activity.contact.first_name} {activity.contact.last_name}\n\n"
        message += "Please take appropriate action.\n\n"
        message += "Sincerely, Your CRM System"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [activity.assigned_to.email],
            fail_silently=True,  # If email sending fails, it won't raise an exception/error message
        )
        print(f"Email sent to {activity.assigned_to.email} for task '{activity.subject}'.")