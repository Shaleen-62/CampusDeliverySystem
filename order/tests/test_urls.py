from django.test import SimpleTestCase
from django.urls import reverse, resolve
from order.views import index, register, user_login, update_cart, cart, checkout, my_orders, search_results, user_logout, delivery_agent


class TestUrls(SimpleTestCase):
    
    def test_index(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)
        
    def test_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)
        
    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, user_login)
        
    # f_id (id of the food item added kept 3 to see if page loaded or not)
    def test_update_cart(self):
        url = reverse('update-cart', args = ['3'])
        self.assertEquals(resolve(url).func, update_cart)
        
    def test_cart(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)
        
    def test_checkout(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)
        
    def test_my_orders(self):
        url = reverse('my-orders')
        self.assertEquals(resolve(url).func, my_orders)
        
    def test_search_results(self):
        url = reverse('search_results')
        self.assertEquals(resolve(url).func, search_results)
        
    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, user_logout)
        
    def test_delivery_agent(self):
        url = reverse('delivery_agent')
        self.assertEquals(resolve(url).func, delivery_agent)
        
        
