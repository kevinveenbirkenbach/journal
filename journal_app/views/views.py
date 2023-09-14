from django.shortcuts import render, get_object_or_404, redirect
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


def index(request):
    return render(request, 'journal_app/index.html', { 'nav_items': getNavigationItems(request)})


