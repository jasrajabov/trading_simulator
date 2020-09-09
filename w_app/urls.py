from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('blotter/', views.Count, name='blotter'),
    path('chart/', views.DispayChart, name='chart'),
    path('quote/', views.Quote, name='quote'),
]
