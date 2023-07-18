from django.contrib import admin
from django.urls import path
from journal_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
    path('add_entry/', views.add_entry, name='add_entry'),
]
