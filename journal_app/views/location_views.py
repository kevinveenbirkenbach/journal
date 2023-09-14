from django.contrib.auth.decorators import login_required
from ..forms import LocationForm
from ..models import Location
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from .common_views import getNavigationItems

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
