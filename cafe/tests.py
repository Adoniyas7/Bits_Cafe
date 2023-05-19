from django.test import TestCase
from .models import  MenuItem, FoodCategory, DailySpecial, Customer
from decimal import Decimal
from django.contrib.auth.models import User
from .forms import CustomerForm
from django.urls import reverse

# Create your tests here.

class MenuItemTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
        MenuItem.objects.create(name="Eggs Benedict", 
                                description="Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.", 
                                price=12.99, 
                                image="https://media.istockphoto.com/id/1291954554/es/foto/huevo-escalfado-en-tostadas-con-manchas-de-yema-de-cerca.jpg?s=1024x1024&w=is&k=20&c=iDW3pN42Ve0msfDLGW8kcCeKQTkbWdJYNRCGhPjP0yw=", 
                                category=FoodCategory.objects.get(name="Breakfast"), 
                                slug="eggs-benedict"
                                )
    def test_menuitem(self):
        eggs_benedict = MenuItem.objects.get(name="Eggs Benedict")
        self.assertEqual(eggs_benedict.description, "Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.")
        self.assertEqual(eggs_benedict.price, Decimal('12.99'))
        self.assertEqual(eggs_benedict.category.name, "Breakfast")
        self.assertEqual(eggs_benedict.slug, "eggs-benedict")

class FoodCategoryTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
    def test_foodcategory(self):
        breakfast = FoodCategory.objects.get(name="Breakfast")
        self.assertEqual(breakfast.name, "Breakfast")

        
class DailySpecialTestCase(TestCase):
    def setUp(self):
        FoodCategory.objects.create(name="Breakfast")
        MenuItem.objects.create(name="Eggs Benedict", 
                                description="Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.", 
                                price=12.99, 
                                image="https://media.istockphoto.com/id/1291954554/es/foto/huevo-escalfado-en-tostadas-con-manchas-de-yema-de-cerca.jpg?s=1024x1024&w=is&k=20&c=iDW3pN42Ve0msfDLGW8kcCeKQTkbWdJYNRCGhPjP0yw=",
                                category=FoodCategory.objects.get(name="Breakfast"), 
                                slug="eggs-benedict", 
                                )
        DailySpecial.objects.create(title="Eggs Benedict", food=MenuItem.objects.get(name="Eggs Benedict"))
    def test_dailyspecial(self):
        eggs_benedict = DailySpecial.objects.get(title="Eggs Benedict")
        self.assertEqual(eggs_benedict.title, "Eggs Benedict")
        self.assertEqual(eggs_benedict.food.name, "Eggs Benedict")

class CustomerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="abebe", password="1234567890")
        Customer.objects.create(user = user, first_name="abebe", last_name="kebede", email="abebe123@gmail.com", phone_number="1234567890")
    def test_customer(self):
        customer = Customer.objects.get(first_name="abebe")
        self.assertEqual(customer.first_name, "abebe")
        self.assertEqual(customer.last_name, "kebede")
        self.assertEqual(customer.email, "abebe123@gmail.com")
        self.assertEqual(customer.phone_number, "1234567890")

class CustomerFormTestCase(TestCase):
    def test_customerform(self):
        data = {
            "username":'abebe',
            "first_name":'abebe',
            "last_name":'kebede',
            "email":'abebe123@gmail.com',
            "phone_number":'0912345678',
            "password1":'123jI(4567890',
            "password2":'123jI(4567890'
        }
        form = CustomerForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'abebe')
        self.assertEqual(form.cleaned_data['first_name'], 'abebe')
        self.assertEqual(form.cleaned_data['last_name'], 'kebede')
        self.assertEqual(form.cleaned_data['email'], 'abebe123@gmail.com')
        self.assertEqual(form.cleaned_data['phone_number'], '0912345678')
        self.assertEqual(form.cleaned_data['password1'], '123jI(4567890')
        self.assertEqual(form.cleaned_data['password2'], '123jI(4567890')



class LoginTest(TestCase):
    def setUp(self):
        self.username = "abebe"
        self.password = "uKD36k95E*4^"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_page(self):
        # Given im on the home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        # When i click on the login button
        response = self.client.get(reverse('login'))
        # Then i should be navigated to the login page
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        # Given im on the login page
        response = self.client.get(reverse('login'))
        # When I enter my username and password and click on the “Login” button
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(reverse('login'), data)
        # Then i should be logged in and redirected to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_fail(self):
        # Given im on the login page
        response = self.client.get(reverse('login'))
        # When I enter a wrong username and password and click on the “Login” button
        data = {'username': self.username, 'password': '12345'}
        response = self.client.post(reverse('login'), data)
        # Then I should see an error message and be prompted to try again
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        
    def test_forgot_password(self):
        # Given im on the login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Password')
        # When i click on the “Reset Password” link
        response = self.client.get(reverse('password_reset'))
        # Then i should be navigated to the “Password Reset” page
        self.assertEqual(response.status_code, 200)

class CartTest(TestCase):
    def setUp(self):
        User.objects.create_user(username="abebe", password="1234567890")
        # Given im logged in as a customer
        self.client.login(username="abebe", password="1234567890")
        FoodCategory.objects.create(name="Breakfast")
        MenuItem.objects.create(name="Eggs Benedict", 
                                description="Eggs Benedict is a dish consisting of two halves of an English muffin topped with Canadian bacon and poached eggs, and covered with a hollandaise sauce.", 
                                price=12.99, 
                                image="https://media.istockphoto.com/id/1291954554/es/foto/huevo-escalfado-en-tostadas-con-manchas-de-yema-de-cerca.jpg?s=1024x1024&w=is&k=20&c=iDW3pN42Ve0msfDLGW8kcCeKQTkbWdJYNRCGhPjP0yw=",
                                category=FoodCategory.objects.get(name="Breakfast"), 
                                slug="eggs-benedict", 
                                )
        DailySpecial.objects.create(title="Eggs Benedict", food=MenuItem.objects.get(name="Eggs Benedict"))


    def test_cart_page(self):
        # When i click on the cart icon
        response = self.client.get(reverse('cart'))
        # Then i should navigate to the cart page
        self.assertEqual(response.status_code, 200)

    def test_empty_cart(self):
        # Given im on the cart page and i have no items in my cart
        # When i scroll through the page
        response = self.client.get(reverse('cart'))
        # Then i should see a message saying "Sorry, Your Cart is Empty. Please add Items!!!"
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sorry, Your Cart is Empty....Please add Items!!!')

    def test_cart_with_items(self):
        # Given im on the cart page and i have items in my cart
        self.client.get(reverse('add_to_cart', args= [MenuItem.objects.get(name="Eggs Benedict").id]))
        # When i scroll through the page
        response = self.client.get(reverse('cart'))
        # Then I should be able to view items in the cart with their name, quantity, price, and total
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eggs Benedict')
        self.assertContains(response, '1')
        self.assertContains(response, '12.99')
        self.assertContains(response, '12.99')

    def test_cart_for_logged_out_user(self):
        # Given im not logged in
        self.client.logout()
        # When i click on the cart icon
        response = self.client.get(reverse('cart'))
        # Then i should be redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/cart/')