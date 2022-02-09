from django.urls import path

from .views import create_staff, create_customer, StaffListView, CustomerListView


urlpatterns = [
    path('create-staff/', create_staff, name='create-staff'),
    path('create-customer/', create_customer, name='create-customer'),

    path('staff-list/', StaffListView.as_view(), name='staff-list'),
    path('customer-list/', CustomerListView.as_view(), name='customer-list'),

]
