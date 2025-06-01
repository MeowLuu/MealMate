from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import MealEvent
from django.db import models
from .forms import MealEventForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import UserProfile
from .forms import ProfileForm
from .models import MealEvent, Participation, UserProfile
from .forms import BillForm,BillUpdateForm
from .models import Bill, Payment
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods
from collections import Counter
from django.core.exceptions import ValidationError
from django.utils.timezone import now



def home(request):
    """Homepage showing all events with search and filter functionality"""
    events = MealEvent.objects.filter(status='active')

    # Search 
    # Search_ Get the info from the url 
    search_query = request.GET.get('search', '')

    if search_query:
        # Q -- OR 
        events = events.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(location__icontains=search_query)
        )

    # Date filter（
    date_filter = request.GET.get('date', '')
    if date_filter:
        events = events.filter(date_time__date=date_filter)  #YYYY-MM-DD

    # Location filter
    location_filter = request.GET.get('location', '')
    if location_filter:
        events = events.filter(location__icontains=location_filter)

    context = {
        'events': events,
        'search_query': search_query,
        'date_filter': date_filter,
        'location_filter': location_filter,
    }

    print(f"[DEBUG] Search query: {search_query}")
    for e in events:
        print(f"[DEBUG] Matched event: {e.title}")
    return render(request, 'MealMate/home.html', context)



@require_http_methods(["GET", "POST"])
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)
    is_participant = Participation.objects.filter(user=request.user, event=event).exists()
    is_host = request.user == event.host

    participants = Participation.objects.filter(event=event).select_related('user') 
    
    preferences = [
        p.user.userprofile.dietary_preferences for p in participants
        if hasattr(p.user, 'userprofile')
    ]
    pref_counts = Counter(preferences)

    # Handle private join from event_detail page
    if request.method == 'POST':
        input_code = request.POST.get('invitation_code', '')
        if input_code == event.invitation_code:
            # Check if event is full
            if event.participants.count() >= event.max_participants:
                messages.error(request, "This event is already full.")
                return redirect('event_detail', event_id=event.id)
            # Check if already joined
            if not Participation.objects.filter(user=request.user, event=event).exists():
                Participation.objects.create(user=request.user, event=event)
                messages.success(request, "You've joined the private event!")
                return redirect('event_detail', event_id=event.id)
            else:
                messages.info(request, "You're already in this event.")
        else:
            messages.error(request, "Invalid invitation code.")

    
    context = {
        "event": event,
        "is_participant": is_participant,
        "is_host": is_host,
        'dietary_data': dict(pref_counts),
    }
    return render(request, 'MealMate/event_detail.html', context)




@login_required
def create_event(request):
    if request.method == 'POST':
        print("POST lat:", request.POST.get('latitude'))
        print("POST lng:", request.POST.get('longitude'))
        form = MealEventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user

            try:
                event.full_clean()  # 
                event.save()
                Participation.objects.create(user=request.user, event=event)
                messages.success(request, 'Done！')
                return redirect('event_detail', event_id=event.id)

            except ValidationError as e:
                form.add_error(None, e)  
                print("ValidationError:", e)

        else:
            print("Form Errors:", form.errors)

    else:
        form = MealEventForm()  

    return render(request, 'MealMate/create_event.html', {'form': form})





@login_required
def my_events(request):
    """Page showing user's hosted and joined events"""
    user = request.user

    # ME as host
    hosted_events = MealEvent.objects.filter(host=user)

    # ME as participants
    joined_events = MealEvent.objects.filter(participation__user=request.user)

    context = {
        'hosted_events': hosted_events,
        'joined_events': joined_events,
    }
    return render(request, 'MealMate/my_events.html', context)

#########
# SignIn - use Django
#########

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify the backend
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'MealMate/signup.html', {'form': form})

#########
# Get Profile
#########

@login_required

def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'MealMate/profile.html', {'form': form, 'profile': profile})

#########
# Edit profile
#########

@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'MealMate/edit_profile.html', {'form': form})

#########
# Test Before Modify
# ✅ Database Worked
#########



@login_required
def join_event(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)

    # Check if event is full
    if event.participants.count() >= event.max_participants:
        messages.error(request, "This event is already full.")
        return redirect('event_detail', event_id=event.id)

    # already joined
    if Participation.objects.filter(user=request.user, event=event).exists():
        messages.info(request, "You're already in this event.")
        return redirect('event_detail', event_id=event.id)

    if event.privacy == 'private':
        input_code = request.POST.get('invitation_code', '')
        if input_code != event.invitation_code:
            messages.error(request, "Invalid invitation code.")
            return redirect('event_detail', event_id=event.id)

    Participation.objects.create(user=request.user, event=event)
    messages.success(request, "You've joined the event!")
    return redirect('event_detail', event_id=event.id)


@login_required
def leave_event(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)

    participation = Participation.objects.filter(event=event, user=request.user).first()
    if not participation:
        messages.warning(request, "You haven't joined this event.")
        return redirect('event_detail', event_id=event.id)

    participation.delete()
    messages.success(request, 'You have withdrawn from this event')
    return redirect('event_detail', event_id=event.id)



@login_required
def edit_event(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)

    # Check host
    if event.host != request.user:
        messages.error(request, 'Only host can edit event')
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = MealEventForm(request.POST, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)

            # Update time from form input
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            updated_event.date_time = datetime.combine(date, time)

            try:
                updated_event.full_clean()  # Will trigger your model's clean()
                updated_event.save()
                messages.success(request, 'Event Updated！')
                return redirect('event_detail', event_id=event.id)
            except ValidationError as e:
                form.add_error(None, e)  # Attach model-level error to form
    else:
        initial = {
            'date': event.date_time.date(),
            'time': event.date_time.time(),
        }
        form = MealEventForm(instance=event, initial=initial)

    return render(request, 'MealMate/create_event.html', {
        'form': form,
        'edit': True,
        'event': event
    })


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)

    if event.host != request.user:
        messages.error(request, 'Please connect with the event host')
        return redirect('event_detail', event_id=event_id)

    event.delete()
    messages.success(request, 'The activity has been successfully deleted.')
    return redirect('my_events')





@login_required
def create_bill(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)


    if hasattr(event, 'bill'):
        messages.warning(request, "Bill already exists for this event.")
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.event = event
            bill.save()

            participants = event.participants.all()
            split_amount = bill.total_amount / participants.count()

            for user in participants:
                Payment.objects.create(
                    bill=bill,
                    user=user,
                    amount=split_amount,
                    status='Pending'
                )
            messages.success(request, "Bill created successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = BillForm()
    
    return render(request, 'MealMate/create_bill.html', {'form': form, 'event': event})


@login_required
def edit_bill(request, event_id):
    event = get_object_or_404(MealEvent, id=event_id)

    if request.user != event.host:
        messages.error(request, "Only the host can edit the bill.")
        return redirect('event_detail', event_id=event.id)

    try:
        bill = event.bill
    except Bill.DoesNotExist:
        messages.error(request, "No bill found to edit.")
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = BillUpdateForm(request.POST, instance=bill)
        if form.is_valid():
            updated_bill = form.save()

          
            Payment.objects.filter(bill=updated_bill).delete()
            participants = event.participants.all()
            new_amount = round(updated_bill.total_amount / participants.count(), 2)

            for user in participants:
                Payment.objects.create(bill=updated_bill, user=user, amount=new_amount, status='Pending')

            messages.success(request, "Bill updated and resplit successfully.")
            return redirect('event_detail', event_id=event.id)
    else:
        form = BillUpdateForm(instance=bill)

    return render(request, 'MealMate/edit_bill.html', {'form': form, 'event': event})
