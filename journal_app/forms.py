from django import forms
from .models import Entry, Location

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['start_time', 'end_time', 'description', 'location', 'parent_entries']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']
