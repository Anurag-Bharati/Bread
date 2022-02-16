from django.test import TestCase, Client
from django.urls import reverse

from manage.models import Customer, Order
from manage.tests.test_views import create_product
from users.models import User

def create_customer():
    user = User.objects.create(username="test_customer")
    user.set_password('123456')
    user.email = 'test_customer'
    user.is_staff = False
    user.is_customer = True
    user.is_admin = False
    user.is_active = True
    user.save()
    customer = Customer.objects.create(
        name='test_customer',
        address='test_address',
        user=user,
    )
    return customer


class TestViews(TestCase):

    order = None
    product = None
    customer = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.customer = create_customer()
        cls.product = create_product()
        cls.order = Order.objects.create(
            product=cls.product,
            quantity=1,
            toppings='test',
            description='test',
            customer=cls.customer,
        )
        cls.home_page_url = reverse('home-page')
        cls.product_page_url = reverse('products')
        cls.order_url = reverse('order', kwargs={'id': cls.order.id})
        cls.my_plate_url = reverse('my-plate')
        cls.profile_url = reverse('customer-profile')
        cls.update_profile_url = reverse('update-profile')

        cls.logout_url = reverse('logout')

    def setUp(self):
        self.client.login(username="test_customer", password="123456")

    def test_home_page(self):
        response = self.client.get(self.home_page_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/home-page/products/')

    def test_get_products(self):
        response = self.client.get(self.product_page_url)
        self.assertEquals(response.status_code, 200)

    def test_customer_get_order(self):
        response = self.client.get(self.order_url)
        self.assertEquals(response.status_code, 200)

    def test_customer_post_order(self):
        response = self.client.post(self.order_url, {
            'quantity': 1,
            'toppings': 'test',
            'description': 'test',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/home-page/my-plate/')

    def test_my_orders(self):
        response = self.client.get(self.my_plate_url)
        self.assertEquals(response.status_code, 200)

    def test_my_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)

    def test_edit_profile(self):
        response = self.client.post(self.update_profile_url, {
            'name': 'test_test',
            'address': 'test',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/home-page/profile/')

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/auth/')

