from django.test import TestCase, Client
from django.urls import reverse

from manage.models import *

def create_staff():
    user = User.objects.create(username="test_staff")
    user.set_password('123456')
    user.email = 'test_staff'
    user.is_staff = True
    user.is_customer = False
    user.is_admin = False
    user.is_active = True
    user.save()
    staff = Staff.objects.create(
        name='test_staff',
        address='test_address',
        user=user,
    )
    return staff

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

def create_product():
    product = Product.objects.create(
        name='test_product',
        type='test',
        price=1,
        desc='test',
        is_featured=False,
        is_special=False,
    )
    return product


class TestViews(TestCase):

    order = None
    customer = None
    product = None
    staff = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
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

        cls.staff_list_url = reverse('staff-list')
        cls.customer_list_url = reverse('customer-list')
        cls.product_list_url = reverse('product-list')
        cls.order_list_url = reverse('order-list')
        cls.delivery_list_url = reverse('delivery-list')

        cls.create_staff_url = reverse('create-staff')
        cls.create_customer_url = reverse('create-customer')
        cls.create_product_url = reverse('create-product')
        cls.create_order_url = reverse('create-order')
        cls.create_delivery_url = reverse('create-delivery')

        cls.edit_order_url = reverse('edit-order', kwargs={'id': cls.order.id})
        cls.delete_order_url = reverse('delete-order', kwargs={'id': cls.order.id})

    def setUp(self):
        self.client.login(username="test_staff", password="123456")

    def test_create_staff(self):
        response = self.client.post(self.create_staff_url, {
            'name': 'test',
            'address': 'test',
            'email': 'test',
            'username': 'test',
            'password': 'test',
            'retype_password': 'test'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/staff-list/')
        self.assertTrue(Staff.objects.filter(name__exact="test") is not None)

    def test_create_customer(self):
        response = self.client.post(self.create_customer_url, {
            'name': 'test',
            'address': 'test',
            'email': 'test',
            'username': 'test',
            'password': 'test',
            'retype_password': 'test'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/customer-list/')
        self.assertTrue(Customer.objects.filter(name__exact="test") is not None)

    def test_create_product(self):
        response = self.client.post(self.create_product_url, {
            'name': 'test',
            'type': 'test',
            'price': 1,
            'desc': 'test',
            'is_featured': False,
            'is_special': False
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/product-list/')
        self.assertTrue(Product.objects.filter(name__exact="test") is not None)

    def test_create_order(self):
        response = self.client.post(self.create_order_url, {
            'staff': self.staff.id,
            'product': self.product.id,
            'quantity': 1,
            'toppings': 'test',
            'description': 'test',
            'customer': self.customer.id,
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/order-list/')
        self.assertTrue(Customer.objects.filter(order__product__name__exact="test_product") is not None)

    def test_edit_order(self):
        response = self.client.post(self.edit_order_url, {
            'staff': self.staff.id,
            'product': self.product.id,
            'customer': self.customer.id,
            'quantity': 2,
            'toppings': 'test',
            'description': 'test',
            'status': 'processing'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/modify-order/')
        self.assertTrue(Customer.objects.filter(order__product__name__exact="test_product") is not None)

    def test_create_delivery(self):
        response = self.client.post(self.create_delivery_url, {
            'order': self.order.id,
            'staff': self.staff.id,
            'remarks': 'Nice',
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/delivery-list/')
        self.assertTrue(Delivery.objects.filter(order__product__name__exact="test_product") is not None)

    def test_delete_order(self):
        response = self.client.delete(self.delete_order_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/manage/modify-order/')

    def test_staff_list(self):
        response = self.client.get(self.staff_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/staff_list.html')

    def test_customer_list(self):
        response = self.client.get(self.customer_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/customer_list.html')

    def test_product_list(self):
        response = self.client.get(self.product_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/product_list.html')

    def test_order_list(self):
        response = self.client.get(self.order_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order_list.html')

    def test_delivery_list(self):
        response = self.client.get(self.delivery_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/delivery_list.html')

    def tearDown(self):
        self.client.logout()
