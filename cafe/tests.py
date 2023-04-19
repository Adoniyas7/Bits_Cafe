from django.test import TestCase
from .models import FoodCategory

# Create your tests here.

class FoodCategoryTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
    def test_foodcategory(self):
        breakfast = FoodCategory.objects.get(name="Breakfast")
        self.assertEqual(breakfast.name, "Breakfast")