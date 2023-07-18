from django.shortcuts import render
from .models import Entry, Location
from .forms import EntryForm, LocationForm

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EntryForm()

    entries = Entry.objects.all()
    return render(request, 'journal_app/index.html', {'form': form, 'entries': entries})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LocationForm()

    locations = Location.objects.all()
    return render(request, 'journal_app/add_location.html', {'form': form, 'locations': locations})
