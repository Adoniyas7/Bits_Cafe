from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null = True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to="menu_images")
    category = models.ForeignKey(FoodCategory, on_delete= models.CASCADE, null = True)
    slug = models.SlugField(max_length=100, unique=True, serialize=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name    
    def get_total(self):
        return self.price * self.quantity
class DailySpecial(models.Model):
    title = models.CharField(max_length=100)
    food = models.ForeignKey(MenuItem, on_delete= models.CASCADE)

    def str(self):
        return self.title
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default.png", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Review(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    review = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null = True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email
    