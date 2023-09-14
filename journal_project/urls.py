from django.contrib import admin
from django.urls import path
from journal_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
    path('add_entry/', views.add_entry, name='add_entry'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('entry/edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('entry/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('filter-entries/', views.filter_entries, name='filter_entries'),
]
