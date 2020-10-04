from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('execute/', views.getOrderDetails, name='execute'),
    path('chart/', views.DispayChart, name='chart'),
    path('quote/', views.Quote, name='quote'),
    path('snippets/', views.trade_list),
    path('snippets/<int:pk>/', views.trade_detail)

]
