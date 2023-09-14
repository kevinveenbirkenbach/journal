from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

class NoAttributSet(ValidationError):
    pass

class TimeFrame(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()
    
    def clean(self):
        if not self.end_time and not self.start_time:
            raise NoAttributSet(_('Start or end time must be set.123'))
        if self.end_time and self.start_time:
            if self.end_time <= self.start_time:
                raise ValidationError(_('End time must be after start time.'))

    def __str__(self):
        return f"{self.start_time} to {self.end_time}"

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()
    
    def clean(self):
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError(_('Latitude must be between -90 and 90.'))
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError(_('Longitude must be between -180 and 180.'))

class Entry(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    parent_entries = models.ManyToManyField('self', blank=True, related_name='sub_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.SET_NULL, null=True, blank=True, related_name='entry')
    history = HistoricalRecords()

    def clean(self):
        if not(self.title or self.description):
            raise ValidationError(_('Title or description must be set.'))
    def __str__(self):
        return f'Entry from {self.time_frame.start_time if self.time_frame else "N/A"} - {self.description[:20]}'
