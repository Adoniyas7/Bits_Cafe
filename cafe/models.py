from django.db import models

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