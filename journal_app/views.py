from django.shortcuts import render
from .models import Entry, Location
from .forms import EntryForm, LocationForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # Set the user
            entry.save()
            form.save_m2m()  # Save many-to-many data if needed
    else:
        form = EntryForm()

    entries = Entry.objects.all()
    return render(request, 'journal_app/index.html', {'form': form, 'entries': entries})

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
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # Set the user
            entry.save()
            form.save_m2m()  # Save many-to-many data if needed
    else:
        form = EntryForm()
    
    entries = Entry.objects.all()
    return render(request, 'journal_app/add_entry.html', {'form': form, 'entries': entries})    
