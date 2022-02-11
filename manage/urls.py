from django.urls import path

from .views import create_staff, create_customer, create_product, create_order, create_delivery, \
    edit_order, StaffListView, CustomerListView, ProductListView, OrderListView, DeliveryListView, \
    ModifyOrder, delete_order

urlpatterns = [

    # CREATE
    path('create-staff/', create_staff, name='create-staff'),
    path('create-customer/', create_customer, name='create-customer'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    # LIST
    path('staff-list/', StaffListView.as_view(), name='staff-list'),
    path('customer-list/', CustomerListView.as_view(), name='customer-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),

    # MODIFY
    path('modify-order/', ModifyOrder.as_view(), name='modify-order'),
    path('edit-order/<int:id>', edit_order, name='edit-order'),
    path('delete-order/<int:id>', delete_order, name='delete-order'),

]
