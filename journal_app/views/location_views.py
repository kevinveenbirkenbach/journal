from django.contrib.auth.decorators import login_required
from ..forms import LocationForm
from ..models import Location
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

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
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LocationForm()

    locations = Location.objects.all()
    return render(request, 'journal_app/add_location.html', {'form': form, 'locations': locations, 'nav_items': getNavigationItems(request)})
