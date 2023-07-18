#!/bin/bash

# Create new Django project named 'journal_project'
django-admin startproject journal_project

cd journal_project

# Create new Django application named 'journal_app'
python manage.py startapp journal_app

# Add 'journal_app' to installed apps in settings.py
echo "INSTALLED_APPS.append('journal_app')" >> journal_project/settings.py

# Generate models.py
echo "from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class Entry(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)" > journal_app/models.py

# Generate forms.py
echo "from django import forms
from .models import Entry, Location

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['start_time', 'end_time', 'description', 'location']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']" > journal_app/forms.py

# Generate views.py
echo "from django.shortcuts import render
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
    return render(request, 'journal_app/add_location.html', {'form': form, 'locations': locations})" > journal_app/views.py

# Create templates directory
mkdir -p journal_app/templates/journal_app

# Create index.html
echo "<form method=\"post\">
    {% csrf_token %}
    {{ form.as_p }}
    <button type=\"submit\">Add Entry</button>
</form>

<ul>
    {% for entry in entries %}
    <li>{{ entry.start_time }} - {{ entry.description }}</li>
    {% endfor %}
</ul>" > journal_app/templates/journal_app/index.html

# Create add_location.html
echo "<form method=\"post\">
    {% csrf_token %}
    {{ form.as_p }}
    <button type=\"submit\">Add Location</button>
</form>

<ul>
    {% for location in locations %}
    <li>{{ location.name }}</li>
    {% endfor %}
</ul>" > journal_app/templates/journal_app/add_location.html

# Generate URLs
echo "from django.contrib import admin
from django.urls import path
from journal_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
]" > journal_project/urls.py

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
