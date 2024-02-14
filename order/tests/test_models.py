from django.test import TestCase
from django.contrib.auth.models import User
from canteen.models import FoodItem
from order.models import Cart, Orders, OrderItems

class TestCart(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        food_item = FoodItem.objects.create(name='Test Food', price=10)
        self.cart = Cart.objects.create(username=user, food=food_item, quantity=2)

    def test_cart_model(self):
        self.assertEqual(self.cart.username.username, 'testuser')
        self.assertEqual(self.cart.food.name, 'Test Food')
        self.assertEqual(self.cart.quantity, 2)

class TestModel(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Orders.objects.create(username=user, total_amount=50, payment_mode='Cash', transaction_id='12345', payment_gateway='Test Gateway')

    def test_orders_model(self):
        self.assertEqual(self.order.username.username, 'testuser')
        self.assertEqual(self.order.total_amount, 50)
        self.assertEqual(self.order.payment_mode, 'Cash')
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.transaction_id, '12345')
        self.assertEqual(self.order.payment_gateway, 'Test Gateway')

class TestOrderItem(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        order = Orders.objects.create(username=user, total_amount=50, payment_mode='Cash', transaction_id='12345', payment_gateway='Test Gateway')
        self.order_item = OrderItems.objects.create(username=user, order=order, name='Test Item', price=10, quantity=2, item_total=20)

    def test_order_items_model(self):
        self.assertEqual(self.order_item.username.username, 'testuser')
        self.assertEqual(self.order_item.order.total_amount, 50)
        self.assertEqual(self.order_item.name, 'Test Item')
        self.assertEqual(self.order_item.price, 10)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.item_total, 20)
