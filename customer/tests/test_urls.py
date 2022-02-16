from django.test import SimpleTestCase
from django.urls import reverse, resolve

from customer.views import *


class TestUrls(SimpleTestCase):

    # Reverse : retrieve url details from url's.py
    # Resolve : resolving URL paths to the corresponding view functions
    # Assert : func/class == func/class

    # Customer Home Page
    def test_base_url_is_resolved(self):
        url = reverse('home-page')
        self.assertEquals(resolve(url).func, home_page)

    def test_product_page_url_is_resolved(self):
        url = reverse('products')
        self.assertEquals(resolve(url).func.view_class, GetProduct)

    def test_order_url_is_resolved(self):
        url = reverse('order', kwargs={'id': 0})
        self.assertEquals(resolve(url).func, order)

    def test_my_plate_url_is_resolved(self):
        url = reverse('my-plate')
        self.assertEquals(resolve(url).func, my_plate)

    def test_profile_url_is_resolved(self):
        url = reverse('customer-profile')
        self.assertEquals(resolve(url).func, my_profile)

    def test_update_profile_url_is_resolved(self):
        url = reverse('update-profile')
        self.assertEquals(resolve(url).func, edit_profile)

