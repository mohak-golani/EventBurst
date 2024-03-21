from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('events/register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('organizer/register/', views.organizer_register, name='organizer_register'),
    path('organizer/login/', views.organizer_login, name='organizer_login'),
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('organizer/logout/', views.organizer_logout, name='organizer_logout'),
    path('past-events/', views.past_events, name='past_events'),
    path('upcoming-events/', views.upcoming_events, name='upcoming_events'),
    path('registered-events/',views.registered_events, name='registered_events'),
]