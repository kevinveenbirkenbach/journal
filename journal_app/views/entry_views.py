from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Entry, NoAttributSet, TimeFrame
from .forms import EntryForm, TimeFrameForm, SearchForm, BulkDeleteForm
from ..utils import getNavigationItems, build_filters_from_form

@method_decorator(login_required, name='dispatch')
class AddEntry(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'journal_app/entry/add_entry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_frame_form'] = TimeFrameForm(self.request.POST or None)
        context['nav_items'] = getNavigationItems(self.request)
        return context

    def post(self, request, *args, **kwargs):
        entry_form = self.form_class(request.POST)
        time_frame_form = TimeFrameForm(request.POST)

        if time_frame_form.is_valid():
            time_frame = time_frame_form.save()
        else:
            time_frame = None

        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = request.user

            if time_frame:
                entry.time_frame = time_frame
                time_frame.save()

            entry.save()
            entry_form.save_m2m()
            return redirect('edit_entry', entry_id=entry.id)

        return render(request, self.template_name, self.get_context_data(form=entry_form))

@method_decorator(login_required, name='dispatch')
class EditEntry(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'journal_app/entry/edit_entry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_object()
        context['time_frame_form'] = TimeFrameForm(instance=entry.time_frame)
        context['nav_items'] = getNavigationItems(self.request)
        return context

    def post(self, request, *args, **kwargs):
        entry = self.get_object()
        entry_form = self.form_class(request.POST, instance=entry)
        
        if entry_form.is_valid():
            entry_form.save()
            return redirect('edit_entry', entry_id=entry.id)

        return render(request, self.template_name, self.get_context_data(form=entry_form))

@method_decorator(login_required, name='dispatch')
class DeleteEntry(DeleteView):
    model = Entry
    template_name = 'journal_app/entry/delete_entry.html'
    success_url = reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_items'] = getNavigationItems(self.request)
        return context

class FilterEntries(ListView):
    model = Entry
    template_name = 'journal_app/filter_entries.html'

    def get_queryset(self):
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            filters = build_filters_from_form(search_form.cleaned_data)
            return Entry.objects.filter(**filters)
        return Entry.objects.all()

    def post(self, request, *args, **kwargs):
        bulk_delete_form = BulkDeleteForm(request.POST)
        if bulk_delete_form.is_valid():
            selected_entries = bulk_delete_form.cleaned_data['selected_entries']
            selected_entries.delete()
        return redirect('filter_entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['bulk_delete_form'] = BulkDeleteForm(self.request.POST or None)
        context['nav_items'] = getNavigationItems(self.request)
        return context
