from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, Location, TimeFrame, NoAttributSet
from .forms import EntryForm, LocationForm, TimeFrameForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

def getNavigationItems(request):
    nav_items = [
        {'url': reverse('index'), 'label': _('Home')},
        {'url': reverse('filter_entries'), 'label': _('Filter Entries')},
    ]

    if request.user.is_authenticated:
        nav_items.extend([
            {'url': reverse('add_location'), 'label': _('Add Location')},
            {'url': reverse('add_entry'), 'label': _('Add Entry')},
            {'url': reverse('logout'), 'label': _('Logout')},
        ])
    else:
        nav_items.append({'url': reverse('login'), 'label': _('Login')})
    return nav_items

@login_required
def profile(request):
    return render(request, 'journal_app/profile.html')

def index(request):
    entries = Entry.objects.all()
    return render(request, 'journal_app/index.html', {'entries': entries, 'nav_items': getNavigationItems(request)})

@login_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LocationForm()

    locations = Location.objects.all()
    return render(request, 'journal_app/add_location.html', {'form': form, 'locations': locations, 'nav_items': getNavigationItems(request)})

def filter_entries(request):
    query_params = ['q', 'start_time', 'end_time', 'start_time_gte', 'start_time_lte', 'end_time_gte', 'end_time_lte']
    if request.method == 'GET':
        filters = {}
        for param in query_params:
            value = request.GET.get(param)
            if value:
                if 'time' in param:
                    try:
                        value = datetime.strptime(value, '%Y-%m-%dT%H:%M')
                        filters[f'time_frame__{param}'] = value
                    except ValueError:
                        pass
                else:
                    filters[f'{param}__icontains'] = value

        filtered_entries = Entry.objects.filter(**filters)
        return render(request, 'journal_app/filter_entries.html', {'filtered_entries': filtered_entries, 'query_params': query_params})

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

    return render(request, 'journal_app/entry/edit_entry.html', {'entry_form': entry_form, 'time_frame_form': TimeFrameForm(instance=entry.time_frame), 'entry': entry, 'nav_items': getNavigationItems(request)})

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
    return render(request, 'journal_app/entry/add_entry.html', {'entry_form': entry_form, 'time_frame_form': time_frame_form, 'nav_items': getNavigationItems(request)})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    
    # Überprüfen Sie, ob der Benutzer der Eigentümer des Eintrags ist
    if entry.user != request.user:
        return HttpResponseForbidden("Sie haben keine Berechtigung, diesen Eintrag zu löschen.")

    if request.method == 'POST':
        entry.delete()
        return redirect('index')  # Nach der Löschung zur Indexseite umleiten

    return render(request, 'journal_app/entry/delete_entry.html', {'entry': entry, 'nav_items': getNavigationItems(request)})

