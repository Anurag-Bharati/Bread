from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


def create_user():
    user = User.objects.create(username="test_customer")
    user.set_password('123456')
    user.email = 'test_customer'
    user.is_staff = True
    user.is_customer = False
    user.is_admin = False
    user.is_active = True
    user.save()

    return user

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = create_user()
        cls.auth_page_url = reverse('auth')
        cls.activated_page_url = reverse('activated')
        cls.logout_url = reverse('logout')

    def setUp(self):
        pass

    def test_auth_page(self):
        response = self.client.get(self.auth_page_url)
        self.assertEquals(response.status_code, 200)

    def test_activated_page(self):
        response = self.client.get(self.activated_page_url)
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/auth/')

    def test_user_login(self):
        response = self.client.post(self.auth_page_url, {
            'username': self.user.username,
            'password': '123456'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')

    def tearDown(self) -> None:
        self.client.logout()
