from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .common_views import getNavigationItems


def index(request):
    return render(request, 'journal_app/index.html', { 'nav_items': getNavigationItems(request)})


