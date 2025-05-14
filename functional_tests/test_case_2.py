from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time

class TestAdvancedCheckoutScenario(StaticLiveServerTestCase):
    
    def setUp(self):
        self.service = webdriver.FirefoxService(executable_path='functional_tests/geckodriver.exe')
        self.browser = webdriver.Firefox(service=self.service)
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def tearDown(self):
        self.browser.close()

    def test_advanced_checkout_scenario(self):
        self.browser.get(self.live_server_url)  

        # Click on log in
        login_url = reverse('login') 
        self.browser.find_element_by_xpath(f"//a[@href='{login_url}']").click()

        # Log in with registered credentials
        self.browser.find_element_by_name('username').send_keys('testuser')
        self.browser.find_element_by_name('password').send_keys('testpassword')
        self.browser.find_element_by_id('submit').click()

        # Search for an item with a substring
        search_query = 'id' 
        self.browser.find_element_by_name('search').send_keys(search_query)
        self.browser.find_element_by_id('search-button').click()

        # Add to cart twice
        add_to_cart_url = reverse('update_cart', args=[1]) 
        self.browser.get(add_to_cart_url)
        self.browser.find_element_by_name('quantity').send_keys('2')
        self.browser.find_element_by_id('add-to-cart').click()

        # Delete one from the existing order
        cart_url = reverse('cart')  
        self.browser.get(cart_url)
        self.browser.find_element_by_name('delete_item').click()

        # Proceed to checkout using Cash on Delivery
        checkout_url = reverse('checkout') 
        self.browser.get(checkout_url)
        self.browser.find_element_by_name('payment_mode').send_keys('Cash')
        self.browser.find_element_by_id('submit').click()

        time.sleep(2)  # Allow some time for the page to process before assertions

        success_message = self.browser.find_element_by_css_selector('.alert-success').text
        self.assertIn('Order Id', success_message)
