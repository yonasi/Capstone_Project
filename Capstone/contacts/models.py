from django.db import models
from django.conf import settings

# company
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# contact
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# activities

from django.db import models
from contacts.models import Contact

class Activity(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.activity_type

# user

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, default='standard') #add role field to default user.

    def __str__(self):
        return self.username