from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .admin import FoodItemAdmin
from .models import FoodItem

class TestAdmin(TestCase):
    
    def setUp(self):
        self.image = SimpleUploadedFile("Best-Pav-Bhaji-Recipe_GcsJV7K_9Yrb0N6.webp", b"file_content", content_type="image/webp")

        # Create a sample FoodItem instance
        self.food_item = FoodItem.objects.create(
            name="Sample Food",
            price=10,
            restaurant="Sample Restaurant",
            image=self.image
        )

        # Create a superuser for authentication
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin_password',
            email='admin@example.com'
        )

        # Create an instance of the FoodItemAdmin
        self.food_item_admin = FoodItemAdmin(FoodItem, AdminSite())

    def test_food_item_admin_list_display(self):
        expected_list_display = ('id', 'name', 'price', 'restaurant', 'image')
        self.assertEqual(self.food_item_admin.list_display, expected_list_display)

    def test_food_item_admin_render_change_form(self):
        request = self.client.get('/admin/canteen/fooditem/{}/change/'.format(self.food_item.id))
        response = self.food_item_admin.render_change_form(request, {}, change=True, obj=self.food_item)
        self.assertEqual(response.status_code, 200)

    def test_food_item_admin_save_model(self):
        request = self.client.post(
            '/admin/canteen/fooditem/{}/change/'.format(self.food_item.id),
            {
                'name': 'Updated Food',
                'price': 15,
                'restaurant': 'Updated Restaurant',
                'image': SimpleUploadedFile("updated_image.jpg", b"updated_content", content_type="image/jpeg")
            }
        )

        updated_food_item = FoodItem.objects.get(id=self.food_item.id)

        self.assertEqual(updated_food_item.name, 'Updated Food')
        self.assertEqual(updated_food_item.price, 15)
        self.assertEqual(updated_food_item.restaurant, 'Updated Restaurant')
        self.assertEqual(updated_food_item.image.name, 'food_pic/updated_image.jpg')
