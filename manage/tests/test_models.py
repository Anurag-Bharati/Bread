from django.test import TestCase

from customer.tests.test_views import create_customer
from manage.models import *
from .test_views import create_staff, create_product

class TestModels(TestCase):

    order = None
    customer = None
    product = None
    staff = None

    @classmethod
    def setUpTestData(cls):
        cls.staff = create_staff()
        cls.customer = create_customer()
        cls.product = create_product()
        cls.order = Order.objects.create(
            staff=cls.staff,
            product=cls.product,
            quantity=1,
            toppings='test',
            description='test',
            customer=cls.customer,
        )
        cls.delivery = Delivery.objects.create(
            staff=cls.staff,
            order=cls.order,
            remarks="delivered"
        )

    def test_order_name_assigned_on_creation(self):
        self.assertEquals(
            self.order.__str__(),
            self.product.name + " by " + self.customer.name
            + " in " + self.order.created_date.__str__()
        )

    def test_token_generation_upon_delivery(self):
        self.assertEquals(
            self.delivery.token,
            Delivery.objects.get(id=self.delivery.id).token
        )
