from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User, Event, EventRegistration

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)
    institution_name = forms.CharField(max_length=100)
    area_of_interest = forms.ChoiceField(choices=Profile.AREA_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'date_of_birth', 'email', 'mobile_number', 'institution_name', 'area_of_interest', 'password1', 'password2')
   
class OrganizerRegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=100)
    organizer_name = forms.CharField(max_length=100)
    organization_address = forms.CharField(widget=forms.Textarea)
    organization_contact = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'organization_name', 'organizer_name', 'organization_address', 'organization_contact')
        
class EventRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = EventRegistration
        fields = ['full_name', 'date_of_birth', 'email', 'mobile_number', 'institution_name']
        
class OrganizerEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'image']