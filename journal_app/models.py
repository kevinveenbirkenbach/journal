from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class Entry(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    parent_entries = models.ManyToManyField('self', blank=True, related_name='sub_entries')

    def __str__(self):
        return f'Entry from {self.start_time} - {self.description[:20]}'

