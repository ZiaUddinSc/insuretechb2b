from django.urls import path
from .views import dashboardCountForCustomer

urlpatterns = [
    path('dashboard/', dashboardCountForCustomer),    
]