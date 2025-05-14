from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import FoodItem

class TestFoodItemModel(TestCase):

    def setUp(self):
        self.image = SimpleUploadedFile("Best-Pav-Bhaji-Recipe_GcsJV7K_9Yrb0N6.webp", b"file_content", content_type="image/jpeg")
        self.food_item = FoodItem.objects.create(
            name="Sample Food",
            price=10,
            restaurant="Sample Restaurant",
            image=self.image
        )

    def test_food_item_creation(self):
        self.assertEqual(self.food_item.name, "Sample Food")
        self.assertEqual(self.food_item.price, 10)
        self.assertEqual(self.food_item.restaurant, "Sample Restaurant")
        self.assertEqual(self.food_item.image.name, "food_pic/test_image.jpg")

    def test_food_item_str_method(self):
        self.assertEqual(str(self.food_item), "Sample Food")
