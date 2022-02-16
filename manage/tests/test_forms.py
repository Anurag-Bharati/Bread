from django.test import SimpleTestCase

from manage.forms import *


class TestForms(SimpleTestCase):

    def test_staff_form_valid_invalid_data(self):
        valid_form = StaffForm(data={
            'name': 'test',
            'address': 'test',
            'email': 'test',
            'username': 'test',
            'password': 'test',
            'retype_password': 'test'
        })
        invalid_form = StaffForm(data={
            'name': 'test',
            'address': 'test',
        })
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 4)

    def test_customer_form_valid_invalid_data(self):
        valid_form = CustomerForm(data={
            'name': 'test',
            'address': 'test',
            'email': 'test',
            'username': 'test',
            'password': 'test',
            'retype_password': 'test'
        })
        invalid_form = CustomerForm(data={
            'name': 'test',
            'address': 12,
        })
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 4)

    def test_product_form_valid_invalid_data(self):
        valid_form = ProductForm(data={
            'name': 'test',
            'type': 'test',
            'price': 1,
            'desc': 'test',
            'is_featured': False,
            'is_special': False,
        })
        invalid_form = ProductForm(data={
            'name': None
        })
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 4)

    def test_order_form_invalid_data(self):
        invalid_form = OrderForm(data={
            'staff': None,
            'customer': None,
            'quantity': 1,
            'product': None,
            'description': 'test',
            'toppings': 'test',
        })
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 3)

    def test_delivery_form_valid_data(self):
        invalid_form = DeliveryForm(data={
            'order': None,
            'staff': None,
            'remarks': 1,
        })
        self.assertFalse(invalid_form.is_valid())
        self.assertEquals(len(invalid_form.errors), 2)
