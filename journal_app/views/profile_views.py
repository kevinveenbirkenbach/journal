from django.views.generic import TemplateView
from ..utils import getNavigationItems

class ProfileView(TemplateView):
    template_name = 'journal_app/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_items'] = getNavigationItems(self.request)
        return context