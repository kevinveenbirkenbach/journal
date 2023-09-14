from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, Location, TimeFrame, NoAttributSet
from .forms import EntryForm, LocationForm, TimeFrameForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

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
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if entry.user != request.user:
        return HttpResponseForbidden(_("The user needs to own the page to edit it"))

    if request.method == 'POST':
        entry_form = EntryForm(request.POST, instance=entry)
        if entry_form.is_valid():
            entry_form.save()
    else:
        entry_form = EntryForm(instance=entry)

    return render(request, 'journal_app/entry/edit_entry.html', {'entry_form': entry_form, 'time_frame_form': TimeFrameForm(instance=entry.time_frame), 'entry': entry})

@login_required
def add_entry(request): 
    time_frame_form = TimeFrameForm(None)
    entry_form = EntryForm(None)
    if request.method == "POST":
        entry_form = EntryForm(request.POST)
        if ('end_time' in request.POST and request.POST['end_time']) or ('start_time' in request.POST and request.POST['start_time']):
            time_frame_form = TimeFrameForm(request.POST)
            pass
        time_frame = None
        try:
            if time_frame_form.is_valid():
                 # Save the TimeFrame instance but don't commit to the database yet
                time_frame = time_frame_form.save()
        except NoAttributSet:
            time_frame_form = TimeFrameForm(None)
        
        if entry_form.is_valid():
           
            
            # Save the Entry instance but don't commit to the database yet
            entry = entry_form.save(commit=False)
            
            if time_frame:
                # Associate the TimeFrame with the Entry
                entry.time_frame = time_frame
                
                # Save the TimeFrame to the database
                time_frame.save()
            
            # Set the user for the Entry
            entry.user = request.user
            
            # Save the Entry to the database
            entry.save()
            
            
            # Save many-to-many data if needed
            entry_form.save_m2m()
    return render(request, 'journal_app/entry/add_entry.html', {'entry_form': entry_form, 'time_frame_form': time_frame_form})

