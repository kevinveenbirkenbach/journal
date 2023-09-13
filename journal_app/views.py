from django.shortcuts import render
from .models import Entry, Location, TimeFrame
from .forms import EntryForm, LocationForm, TimeFrameForm
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'journal_app/profile.html')

def index(request):
    entries = Entry.objects.all()
    return render(request, 'journal_app/index.html', {'entries': entries})

@login_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LocationForm()

    locations = Location.objects.all()
    return render(request, 'journal_app/add_location.html', {'form': form, 'locations': locations})

@login_required
def add_entry(request):
    time_frame_form = TimeFrameForm(request.POST or None)
    entry_form = EntryForm(request.POST or None)

    if request.method == "POST":
        if time_frame_form.is_valid() and entry_form.is_valid():
            # Save the TimeFrame instance but don't commit to the database yet
            time_frame = time_frame_form.save()
            
            # Save the Entry instance but don't commit to the database yet
            entry = entry_form.save(commit=False)
            
            # Associate the TimeFrame with the Entry
            entry.time_frame = time_frame
            
            # Set the user for the Entry
            entry.user = request.user
            
            # Save the Entry to the database
            entry.save()
            
            # Save the TimeFrame to the database
            time_frame.save()
            
            # Save many-to-many data if needed
            entry_form.save_m2m()

    entries = Entry.objects.all()
    return render(request, 'journal_app/add_entry.html', {'entry_form': entry_form, 'time_frame_form': time_frame_form, 'entries': entries})

