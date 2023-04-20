from django.test import TestCase
from .models import  MenuItem, FoodCategory
from decimal import Decimal

# Create your tests here.

class MenuItemTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
        MenuItem.objects.create(name="Eggs Benedict", 
                                description="Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.", 
                                price=12.99, 
                                image="https://media.istockphoto.com/id/1291954554/es/foto/huevo-escalfado-en-tostadas-con-manchas-de-yema-de-cerca.jpg?s=1024x1024&w=is&k=20&c=iDW3pN42Ve0msfDLGW8kcCeKQTkbWdJYNRCGhPjP0yw=", 
                                category=FoodCategory.objects.get(name="Breakfast"), 
                                slug="eggs-benedict", 
                                quantity=1
                                )
    def test_menuitem(self):
        eggs_benedict = MenuItem.objects.get(name="Eggs Benedict")
        self.assertEqual(eggs_benedict.description, "Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.")
        self.assertEqual(eggs_benedict.price, Decimal('12.99'))
        self.assertEqual(eggs_benedict.category.name, "Breakfast")
        self.assertEqual(eggs_benedict.slug, "eggs-benedict")
        self.assertEqual(eggs_benedict.quantity, 1)

class FoodCategoryTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
    def test_foodcategory(self):
        breakfast = FoodCategory.objects.get(name="Breakfast")
        self.assertEqual(breakfast.name, "Breakfast")