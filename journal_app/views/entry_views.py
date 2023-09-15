from django.shortcuts import render, get_object_or_404, redirect
from journal_app.models import Entry, TimeFrame, NoAttributSet
from journal_app.forms import EntryForm, TimeFrameForm, SearchForm, BulkDeleteForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .common_views import getNavigationItems
from rest_framework import generics
from journal_app.serializers import EntrySerializer

class EntryListCreateView(generics.ListCreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

class EntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

def list_entries(request):
    search_form = SearchForm(request.GET)
    bulk_delete_form = BulkDeleteForm(request.POST or None)

    if request.method == 'GET' and search_form.is_valid():
        filters = build_filters_from_form(search_form.cleaned_data)
        filtered_entries = Entry.objects.filter(**filters)
    else:
        filtered_entries = Entry.objects.all()

    if request.method == 'POST' and bulk_delete_form.is_valid():
        selected_entries = bulk_delete_form.cleaned_data['selected_entries']
        selected_entries.delete()

    context = {
        'filtered_entries': filtered_entries,
        'bulk_delete_form': bulk_delete_form,
        'search_form': search_form,
        'nav_items': getNavigationItems(request),
    }
    return render(request, 'journal_app/entry/entries_list.html', context)

def build_filters_from_form(cleaned_data):
    filters = {}

    filter_mapping = {
        'title': 'title__icontains',
        'description': 'description__icontains',
        'time_frame__start_time': 'time_frame__start_time',
        'time_frame__end_time': 'time_frame__end_time',
        'time_frame__start_time_gte': 'time_frame__start_time__gte',
        'time_frame__end_time_gte': 'time_frame__end_time__gte',
        'time_frame__start_time_lte': 'time_frame__start_time__lte',
        'time_frame__end_time_lte': 'time_frame__end_time__lte',
    }

    for field_name, filter_key in filter_mapping.items():
        field_value = cleaned_data.get(field_name)
        if field_value:
            filters[filter_key] = field_value

    return filters

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
    status_code = 200
    if request.method == "POST":
        status_code = 201
        entry_form = EntryForm(request.POST)
        if ('end_time' in request.POST and request.POST['end_time']) or ('start_time' in request.POST and request.POST['start_time']):
            time_frame_form = TimeFrameForm(request.POST)
        time_frame = None
        try:
            status_code = 207
            if time_frame_form.is_valid():
                 # Save the TimeFrame instance but don't commit to the database yet
                time_frame = time_frame_form.save()
                status_code = 201
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
            
            # Redirect 
            response = redirect('edit_entry', entry_id=entry.id)
            response.status_code = status_code
            return response
        else:
            status_code=400
    return render(request, 'journal_app/entry/add_entry.html', {'entry_form': entry_form, 'time_frame_form': time_frame_form, 'nav_items': getNavigationItems(request)},status=status_code)

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