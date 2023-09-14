from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from .common_views import getNavigationItems

@login_required
def profile(request):
    return render(request, 'journal_app/profile.html')
