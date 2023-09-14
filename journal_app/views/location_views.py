from django.views.generic.edit import CreateView
from .models import Location
from .forms import LocationForm
from ..utils import getNavigationItems

class AddLocation(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'journal_app/add_location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['nav_items'] = getNavigationItems(self.request)
        return context