from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Event, Category, Participant
from .forms import EventForm, ParticipantForm, CategoryForm
from .models import Event
from django.utils.timezone import now
from django.http import JsonResponse

from django.db.models import Q 

# -----------------------
# HOME VIEW
# -----------------------
def home(request):
    query = request.GET.get('search', '')  # Get search query from URL
    events = Event.objects.all()  # Get all events by default

    if query:
        events = events.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

    return render(request, "events.html", {"events": events, "query": query})

# -----------------------
# EVENT VIEWS (CRUD)
# -----------------------
def event_list(request):
    events = Event.objects.all()
    print(events)  # Debugging: Check if new events are appearing
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
        else:
            print(form.errors)  # Debugging: Check if form has errors
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})

# -----------------------
# PARTICIPANT VIEWS (CRUD)
# -----------------------
def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participant_list.html', {'participants': participants})

def participant_detail(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    return render(request, 'participant_detail.html', {'participant': participant})

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

def participant_update(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})

def participant_delete(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})

# -----------------------
# CATEGORY VIEWS (CRUD)
# -----------------------
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category_detail.html', {'category': category})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

# -----------------------
# DASHBOARD VIEW (With Optimized Queries)
# -----------------------
def dashboard(request):
    total_participants = Participant.objects.count()  # Example, replace with actual query
    total_events = Event.objects.count()
    
    today = now().date()
    today_events = Event.objects.filter(date=today)
    upcoming_events = Event.objects.filter(date__gte=today)  # Future events
    past_events = Event.objects.filter(date__lt=today)  # Past events

    context = {
        "total_participants": total_participants,
        "total_events": total_events,
        "today_events": today_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,  # Fix: Ensure this is a queryset, not an integer
    }
    return render(request, "dashboard.html", context)

# NEW: API for fetching filtered events (ADD THIS)
def get_filtered_events(request):
    filter_type = request.GET.get("filter", "today")
    
    if filter_type == "upcoming":
        events = Event.objects.filter(date__gte=now().date())
    elif filter_type == "past":
        events = Event.objects.filter(date__lt=now().date())
    elif filter_type == "all":
        events = Event.objects.all()
    else:  # Default to today's events
        events = Event.objects.filter(date=now().date())

    event_data = [{"name": event.name, "date": event.date.strftime("%Y-%m-%d")} for event in events]
    
    return JsonResponse({"events": event_data})
# -----------------------
# SEARCH FUNCTIONALITY
# -----------------------
 # Import Q for complex queries

def event_search(request):
    query = request.GET.get('q', '')  # Get search query, default to empty string
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = Event.objects.all()
    
    return render(request, 'event_list.html', {'events': events})