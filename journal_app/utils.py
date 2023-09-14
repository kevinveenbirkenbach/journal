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
