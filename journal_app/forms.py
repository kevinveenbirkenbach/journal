from django import forms
from .models import Entry, Location, TimeFrame

class TimeFrameForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    
    class Meta:
        model = TimeFrame
        fields = ['start_time', 'end_time']

class EntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), required=False)
    
    class Meta:
        model = Entry
        fields = ['title', 'description', 'location', 'parent_entries']

class LocationForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'min': '-90', 'max': '90'}))
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'min': '-180', 'max': '180'}))
    
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']
        
class BulkDeleteForm(forms.Form):
    selected_entries = forms.ModelMultipleChoiceField(queryset=Entry.objects.all(), widget=forms.CheckboxSelectMultiple)
