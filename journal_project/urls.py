from django.contrib import admin
from django.urls import path
from journal_app.views import views, entry_views, profile_views, location_views
from django.contrib.auth import views as auth_views
from journal_app.views.entry_views import EntryListCreateView, EntryRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_location/', location_views.add_location, name='add_location'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile_views.profile, name='profile'),
    path('entry/add', entry_views.add_entry, name='add_entry'),  # Verwenden Sie entry_views hier
    path('entry/edit/<int:entry_id>/', entry_views.edit_entry, name='edit_entry'),  # ... und hier
    path('entry/delete/<int:entry_id>/', entry_views.delete_entry, name='delete_entry'),  # ... und hier
    path('entry/list', entry_views.list_entries, name='list_entries'),
    # API
    path('api/entry/', EntryListCreateView.as_view(), name='api_entry_list_create'),
    path('api/entry/<int:pk>/', EntryRetrieveUpdateDestroyView.as_view(), name='api_entry_retrieve_update_destroy'),
    path('search_entries/', views.search_entries, name='search_entries'),
]
