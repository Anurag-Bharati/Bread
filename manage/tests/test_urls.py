from django.test import SimpleTestCase
from django.urls import reverse, resolve

from manage.views import *


class TestUrls(SimpleTestCase):

    # Reverse : retrieve url details from url's.py
    # Resolve : resolving URL paths to the corresponding view functions
    # Assert : func/class == func/class

    # Create
    def test_create_staff_url_is_resolved(self):
        url = reverse('create-staff')
        self.assertEquals(resolve(url).func, create_staff)

    def test_create_customer_url_is_resolved(self):
        url = reverse('create-customer')
        self.assertEquals(resolve(url).func, create_customer)

    def test_create_product_url_is_resolved(self):
        url = reverse('create-product')
        self.assertEquals(resolve(url).func, create_product)

    def test_create_order_url_is_resolved(self):
        url = reverse('create-order')
        self.assertEquals(resolve(url).func, create_order)

    def test_create_delivery_url_is_resolved(self):
        url = reverse('create-delivery')
        self.assertEquals(resolve(url).func, create_delivery)

    # LIST
    def test_staff_list_url_is_resolved(self):
        url = reverse('staff-list')
        self.assertEquals(resolve(url).func.view_class, StaffListView)

    def test_customer_list_url_is_resolved(self):
        url = reverse('customer-list')
        self.assertEquals(resolve(url).func.view_class, CustomerListView)

    def test_product_list_url_is_resolved(self):
        url = reverse('product-list')
        self.assertEquals(resolve(url).func.view_class, ProductListView)

    def test_order_list_url_is_resolved(self):
        url = reverse('order-list')
        self.assertEquals(resolve(url).func.view_class, OrderListView)

    def test_delivery_list_url_is_resolved(self):
        url = reverse('delivery-list')
        self.assertEquals(resolve(url).func.view_class, DeliveryListView)

    # MOD
    def test_mod_order_url_is_resolved(self):
        url = reverse('modify-order')
        self.assertEquals(resolve(url).func.view_class, ModifyOrder)

    def test_mod_product_url_is_resolved(self):
        url = reverse('modify-product')
        self.assertEquals(resolve(url).func.view_class, ModifyProduct)

    def test_edit_order_url_is_resolved(self):
        url = reverse('edit-order', kwargs={'id': 0})
        self.assertEquals(resolve(url).func, edit_order)

    def test_edit_product_url_is_resolved(self):
        url = reverse('edit-product', kwargs={'id': 0})
        self.assertEquals(resolve(url).func, edit_product)

    def test_delete_order_url_is_resolved(self):
        url = reverse('delete-order', kwargs={'id': 0})
        self.assertEquals(resolve(url).func, delete_order)

    def test_delete_product_url_is_resolved(self):
        url = reverse('delete-product', kwargs={'id': 0})
        self.assertEquals(resolve(url).func, delete_product)

    # MISC
    def test_order_summary_url_is_resolved(self):
        url = reverse('order-summary')
        self.assertEquals(resolve(url).func, order_summary)
