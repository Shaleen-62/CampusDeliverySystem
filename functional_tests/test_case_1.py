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
        self.browser.get(self.live_server_url)  # Replace with your home page URL

        # Click on log in
        login_url = reverse('login')  # Replace with your actual login URL
        self.browser.find_element_by_xpath(f"//a[@href='{login_url}']").click()

        # Log in with unprecedented credentials
        self.browser.find_element_by_name('username').send_keys('unprecedented')
        self.browser.find_element_by_name('password').send_keys('wrongpassword')
        self.browser.find_element_by_id('submit').click()

        # Register new credentials
        register_url = reverse('register')  # Replace with your actual registration URL
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
        add_to_cart_url = reverse('add_to_cart', args=[1])  # Replace with your actual add to cart URL
        self.browser.get(add_to_cart_url)

        # Proceed to checkout using Cash on Delivery
        checkout_url = reverse('checkout')  # Replace with your actual checkout URL
        self.browser.get(checkout_url)
        self.browser.find_element_by_name('payment_mode').send_keys('Cash')
        self.browser.find_element_by_id('submit').click()

        # Optionally, you can add assertions to check the success message or the state of your models
        time.sleep(2)  # Allow some time for the page to process before assertions

        # Example assertion - check for success message on the checkout page
        success_message = self.browser.find_element_by_css_selector('.alert-success').text
        self.assertIn('Order placed successfully!', success_message)
