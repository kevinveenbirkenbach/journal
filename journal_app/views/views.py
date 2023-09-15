from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .common_views import getNavigationItems
from journal_app.models import Entry


def index(request):
    return render(request, 'journal_app/index.html', { 'nav_items': getNavigationItems(request)})

from django.http import JsonResponse

def search_entries(request):
    query = request.GET.get('query')
    entries = Entry.objects.filter(title__icontains=query)[:5]  # Nehmen wir nur die ersten 5 Ergebnisse an
    results = [{"id": entry.id, "title": entry.title} for entry in entries]
    return JsonResponse(results, safe=False)



