from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home'),
    path('execute/', views.getOrderDetails, name='execute'),
    path('quote/', views.Quote, name='quote'),
    path('trades/', views.trade_list, name='trades'),
    path('trades/<int:id>/', views.trade_detail, name='single_trade')

]

urlpatterns = format_suffix_patterns(urlpatterns)
