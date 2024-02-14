from django.test import TestCase, Client
from django.contrib.auth.models import User
from canteen.models import FoodItem
from order.models import Cart, Orders, OrderItems
from order.forms import LoginRegisterForm
from django.urls import reverse

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Test registration with valid data
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration

        # Test registration with existing username
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to registration page due to existing username

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Test login with valid credentials
        User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

        # Test login with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to login page due to invalid credentials
