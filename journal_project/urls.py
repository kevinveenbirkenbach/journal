from django.contrib import admin
from django.urls import path
from journal_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_location/', views.add_location, name='add_location'),
    path('add_entry/', views.add_entry, name='add_entry'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
