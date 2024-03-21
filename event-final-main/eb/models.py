from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_current = models.BooleanField(default=False)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=100)
    AREA_CHOICES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Art', 'Art'),
        ('Sports', 'Sports'),
        # Add more choices as needed
    ]
    area_of_interest = models.CharField(max_length=50, choices=AREA_CHOICES)

    def __str__(self):
        return self.user.username
    
class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100)
    organizer_name = models.CharField(max_length=100)
    organization_address = models.TextField()
    organization_contact = models.CharField(max_length=15)
    
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=100)
