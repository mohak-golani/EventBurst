from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, Profile, OrganizerProfile
from .forms import RegistrationForm, EventRegistrationForm, OrganizerRegistrationForm, OrganizerEventForm

def home(request):
    return render(request, 'home.html')

def events(request):
    past_events = Event.objects.filter(end_date__lt=timezone.now(), is_current=False)
    #current_events = Event.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
    current_events = Event.objects.filter(is_current=True)
    upcoming_events = Event.objects.filter(start_date__gt=timezone.now(), is_current=False)
    return render(request, 'events.html', {'past_events': past_events, 'current_events': current_events, 'upcoming_events': upcoming_events})

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            email = form.cleaned_data.get('email')
            mobile_number = form.cleaned_data.get('mobile_number')
            institution_name = form.cleaned_data.get('institution_name')
            area_of_interest = form.cleaned_data.get('area_of_interest')
            Profile.objects.create(user=user, full_name=full_name, date_of_birth=date_of_birth, email=email, mobile_number=mobile_number, institution_name=institution_name, area_of_interest=area_of_interest)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)#, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect user to their respective dashboard based on category
            profile = Profile.objects.get(user=user)
            '''if profile.category.name == 'Driver':
                return redirect('dashboard_driver')
            elif profile.category.name == 'Rider':
                return redirect('dashboard_rider')
            elif profile.category.name == 'Owner':
                return redirect('dashboard_owner')
            elif profile.category.name == 'Tenant':
                return redirect('dashboard_tenant')'''
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@login_required
def dashboard(request):
    # Get the username
    username = request.user.username
    
    # Retrieve past, current, and upcoming events
    past_events = Event.objects.filter(end_date__lt=timezone.now(), is_current=False)
    current_events = Event.objects.filter(is_current=True)
    upcoming_events = Event.objects.filter(start_date__gt=timezone.now(), is_current=False)
    
    # Retrieve registered events for the current user
    registered_events = Event.objects.filter(eventregistration__user=request.user)
    
    return render(request, 'dashboard.html', {'past_events': past_events, 'current_events': current_events, 'upcoming_events': upcoming_events, 'registered_events': registered_events, 'username': username})



def register_for_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            # Save the registration data
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            return redirect('events')  # Redirect to events page after registration
    else:
        form = EventRegistrationForm()
    return render(request, 'register_for_event.html', {'form': form, 'event': event})

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('home')

#--------------------------------------:) Organizer's Seperate logic ;)-----------------------------------
def organizer_register(request):
    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            organization_name = form.cleaned_data.get('organization_name')
            organizer_name = form.cleaned_data.get('organizer_name')
            organization_address = form.cleaned_data.get('organization_address')
            organization_contact = form.cleaned_data.get('organization_contact')
            OrganizerProfile.objects.create(user=user, organization_name=organization_name, organizer_name=organizer_name, organization_address=organization_address, organization_contact=organization_contact)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('organizer_dashboard')
    else:
        form = OrganizerRegistrationForm()
    return render(request, 'organizer_register.html', {'form': form})

def organizer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if OrganizerProfile.objects.filter(user=user).exists():
                auth_login(request, user)
                return redirect('organizer_dashboard')
            else:
                messages.error(request, 'Invalid credentials for organizer.')
    else:
        form = AuthenticationForm()
    return render(request, 'organizer_login.html', {'form': form})

@login_required
def organizer_dashboard(request):
    if request.method == 'POST':
        form = OrganizerEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user.organizerprofile  # Assuming OrganizerProfile is related to User
            event.save()
            return redirect('organizer_dashboard')
    else:
        form = OrganizerEventForm()
    return render(request, 'organizer_dashboard.html', {'form': form})

@login_required
def organizer_logout(request):
    auth_logout(request)
    return redirect('home')
def contact_us(request):
    return render(request, 'contact_us.html')
def past_events(request):
    return render(request, 'past_events.html')
def upcoming_events(request):
    return render(request, 'upcoming_events.html')
def registered_events(request):
    return render(request, 'registered_events.html')