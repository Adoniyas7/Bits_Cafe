from django.db import models

# Create your models here.
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"
    def __str__(self):
        return self.name