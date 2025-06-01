from django.contrib import admin
from django.urls import path
from MealMate import views
from django.contrib.auth import views as auth_views  
from django.urls import path, include
from allauth.account import views as allauth_views
from allauth.account.views import LoginView 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'),
    path("create/", views.create_event, name='create_event'),
    path("event/<int:event_id>/", views.event_detail, name='event_detail'),
    path("event/<int:event_id>/join/", views.join_event, name='join_event'),
    path("event/<int:event_id>/leave/", views.leave_event, name='leave_event'),
    path("event/<int:event_id>/edit/", views.edit_event, name='edit_event'),
    path("event/<int:event_id>/delete/", views.delete_event, name='delete_event'),
    path("my-events/", views.my_events, name='my_events'),

    # For login/logout

    #path("login/", auth_views.LoginView.as_view(template_name='MealMate/login.html'), name='login'),

    path("login/", LoginView.as_view(template_name='MealMate/login.html'), name='login'),
    
   

    path(
    "logout/",
    auth_views.LogoutView.as_view(template_name="MealMate/logout.html"),
    name="logout"
    ),

    path('signup/', views.signup, name='signup'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('event/<int:event_id>/create-bill/', views.create_bill, name='create_bill'),

    path('event/<int:event_id>/edit-bill/', views.edit_bill, name='edit_bill'),

    path('accounts/', include('allauth.urls')),



]
