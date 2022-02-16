from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import authenticate, activated, verification, logout

class TestUrls(SimpleTestCase):

    # Reverse : retrieve url details from url's.py
    # Resolve : resolving URL paths to the corresponding view functions
    # Assert : func/class == func/class

    def test_auth_url_is_resolved(self):
        url = reverse('auth')
        self.assertEquals(resolve(url).func, authenticate)

    def test_account_activated_is_resolved(self):
        url = reverse('activated')
        self.assertEquals(resolve(url).func, activated)

    def test_activate_account_is_resolved(self):
        url = reverse('activate', kwargs={'identity': None, 'token': None})
        self.assertEquals(resolve(url).func, verification)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
