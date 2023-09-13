from django import forms
from .models import Entry, Location, TimeFrame

class TimeFrameForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = TimeFrame
        fields = ['start_time', 'end_time']

class EntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea())
    
    class Meta:
        model = Entry
        fields = ['description', 'location', 'parent_entries']

class LocationForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'min': '-90', 'max': '90'}))
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'min': '-180', 'max': '180'}))
    
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']
