from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time

class TestCheckoutScenario(StaticLiveServerTestCase):
    
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

    def test_checkout_scenario(self):
        # Open home page
        self.browser.get(self.live_server_url) 

        # Click on log in
        login_url = reverse('login')  
        self.browser.find_element_by_xpath(f"//a[@href='{login_url}']").click()

        # Log in with unprecedented credentials
        self.browser.find_element_by_name('username').send_keys('unprecedented')
        self.browser.find_element_by_name('password').send_keys('wrongpassword')
        self.browser.find_element_by_id('submit').click()

        # Register new credentials
        register_url = reverse('register') 
        self.browser.find_element_by_xpath(f"//a[@href='{register_url}']").click()
        self.browser.find_element_by_name('username').send_keys('newuser')
        self.browser.find_element_by_name('password1').send_keys('newpassword')
        self.browser.find_element_by_name('password2').send_keys('newpassword')
        self.browser.find_element_by_id('submit').click()

        # Log in with the new credentials
        self.browser.find_element_by_name('username').send_keys('newuser')
        self.browser.find_element_by_name('password').send_keys('newpassword')
        self.browser.find_element_by_id('submit').click()

        # Add item with id 1 to the cart
        add_to_cart_url = reverse('update_cart', args=[1])  
        self.browser.get(add_to_cart_url)

        # Proceed to checkout using Cash on Delivery
        checkout_url = reverse('checkout') 
        self.browser.get(checkout_url)
        self.browser.find_element_by_name('payment_mode').send_keys('Cash')
        self.browser.find_element_by_id('submit').click()

        time.sleep(2)  # Allow some time for the page to process before assertions

        success_message = self.browser.find_element_by_css_selector('.alert-success').text
        self.assertIn('Order Id', success_message)
